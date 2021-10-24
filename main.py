import argparse,  sma

from modbus import Modbus
from logger import TableLogger
from openhablogger import OpenhabLogger

parser = argparse.ArgumentParser(description='Gather data of your sma inverter')
parser.add_argument('registers',
                    type=int,
                    nargs='*',
                    help='list of register numbers')
parser.add_argument('-d', '--daemon',
                    action='store_true',
                    default=False,
                    help='keep polling')
parser.add_argument('-i', '--interval',
                    type=int,
                    default=60,
                    help='time in seconds between polls')
parser.add_argument('-l', '--list',
                    action='store_true',
                    help='list all registers')
parser.add_argument('-log', '--log',
                    action='store_true',
                    help='log results in table-format')
parser.add_argument('-a', '--adress',
                    type=str,
                    help='modbus-TCP ip-adress')
parser.add_argument('-p', '--port',
                    type=int, 
                    default= 502,
                    help='modbus-TCP ip-port, default: 502')
parser.add_argument('-u', '--unit',
                    type=int, 
                    default= 3,
                    help='modbus unit, default: 3')
'''
parser.add_argument('-t', '--type',
                    type=str,
                    required=True,
                    help='inverter type')
'''
parser.add_argument('-all','--all',
                    action='store_true',
                    help='Read All Registers')

parser.add_argument('-f','--file', 
                    type=argparse.FileType('r'),
                    help='Read the registers from the file, the registers must separated with line break')

parser.add_argument('--ohitems',
                    action='store_true',
                    help='Print the Openhab items for the registers, use the register file for nice formatting')

parser.add_argument('--ohlogport',
                    type=int,
                    default=8080,
                    help='Port of the Openhab-Server where the results will be written')

parser.add_argument('-o', '--ohlog',
                    type=str,
                    help='Log to Openhab; IP/Url of of the Openhab-Server where the results will be written')

args = parser.parse_args()

# check args
if not args.registers and not args.all and not args.list and not args.file:
    print("Registers or File with Registers or Mode 'List' or Mode 'All' required! \n")
    parser.print_help()
    exit()

if not args.list and not args.adress:
    print("Adress of the inverter is required! \n")
    parser.print_help()
    exit()

logger = None

if args.ohlog:
    logger = OpenhabLogger(args.ohlog, args.ohlogport)
elif args.log:
    logger = TableLogger()

wr = Modbus(ipAdress=args.adress, ipPort=args.port, modbusUnit=args.unit, 
                runAsDaemon=args.daemon, pollingInterval=args.interval, logger= logger)

#import register definitions
sma.add_tripower_register(wr)
sma.set_tripower_TAGLIST()

''' See SMA.py there are some bugs for the other inverters
if args.type == "tripower":
    add_tripower_register(wr)
elif args.type == "sbstorage":
    add_sbstorage_register(wr)
elif args.type == "sbxx-1av-41":
    add_sbxx_1av_41_register(wr)
else:
    sys.exit("Unknown inverter type.")
'''

lines = None

if args.list:
    wr.list_available_registers()
    exit()
elif args.all:
    for register in wr.available_registers.keys():
        wr.poll_register(register)
elif args.file:
    lines = [line for line in args.file.readlines() if line.strip()!='']
    for r in lines:
        if r[0]=='#': 
            continue
        wr.poll_register(int(r))
else:
    for register in args.registers:
        wr.poll_register(register)
    
if args.ohitems:
    if lines:        
        for l in lines:
            if l[0]=='#':
                print("\n",r"// ", l[1:].strip())
            else:
                print( wr.available_registers[int(l)].get_openhab_item())
    else:    
        for id in wr.registers:
            print( wr.available_registers[id].get_openhab_item())
    print("\n\n\n")

wr.start()
