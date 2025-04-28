# py-sma-modbus2
Read out *all* values (eg MPPT1 und MPPT2,...) from SMA inverters in local network via Modbus TCP. You don't need the SMA Sunny Portal anymore.

Tested with SMA Tripower STP 20000TL-30 and Python 3.10/3.11 under Windows 11 and Debian 12 "bookworm"

*new*: Updated to pymodbus V3.9.2

This is a fork of **py-sma-modbus** and **Wy53/py-sma-modbus**:
- fixed bugs with signed int registers and string registers
- removed the "GUI" (problems under Windows)
- more robust daemon with systemd under linux
- a bit more pythonic
- values in correct dimension with units
- all types and TAGLIST are supported
- nice formatting with automatic unit prefixes 
- load registers from file
- output values to OpenHab REST web service (1.x)
- output values to InfluxDB 1.x (output registers to JSON)


## Todo
- Write Registers
- Register description and TAGLIST in English or other language

## Installation

1) Enable with the SMA tool "Sunny Explorer" the *Modbus TCP* protocol on the inverter (UDP is not needed)
2) Make sure that the inverter has a static IP Adress (or always gets the same IP via DHCP)
3) Download the code or clone it:
```sh
git clone git@github.com:stefanlsa/py-sma-modbus2.git
cd py-sma-modbus2
```
4) Create a virtual envrionment activate it and install requirements: 
```sh
python3 -m venv run/
source run/bin/activate
pip install -r requirements.txt
```
5) Optional: Run it as a daemon under linux, as root do (or sudo):
 - copy sma.service to /etc/systemd/system
 - edit the lines ExecStart and WorkingDirectory to make sure that the service will point in the correct directory
 - edit the line USER in woch context the demon will run eg. the user from openhab installation
 - Reload the service files to include the new service.
 ```sh
 $ systemctl daemon-reload
 ```
 - Start your service
 ```sh
 $ systemctl start sma.service
 ```
 - To enable your service on every reboot
 ```sh
 $ systemctl enable sma.service
 ```
 -To check the status of your service
 ```sh
 $ systemctl status sma.service
 ```



## Usage

```sh
usage: main.py [-h] [-d] [-i INTERVAL] [-l] [-log] [-a ADRESS] [-p PORT]
               [-u UNIT] [-all] [-f FILE] [--ohitems] [--logport OHLOGPORT]
               [-o OHLOG] [-influxlog INFLUXLOG]
               [registers [registers ...]]

Gather data of your sma inverter

positional arguments:
  registers             list of register numbers

optional arguments:
  -h, --help            show this help message and exit
  -d, --daemon          keep polling
  -i INTERVAL, --interval INTERVAL
                        time in seconds between polls
  -l, --list            list all registers
  -log, --log           log results in table-format
  -a ADRESS, --adress ADRESS
                        modbus-TCP ip-adress
  -p PORT, --port PORT  modbus-TCP ip-port, default: 502
  -u UNIT, --unit UNIT  modbus unit, default: 3
  -all, --all           Read All Registers
  -f FILE, --file FILE  Read the registers from the file, the registers must
                        separated with line break
  --ohitems             Print the Openhab items for the registers, use the
                        register file for nice formatting
  --logport OHLOGPORT
                        Port of the Openhab-Server or InfluxDB where the results will be
                        written
  -o OHLOG, --ohlog OHLOG
                        Log to Openhab; IP/Url of of the Openhab-Server where
                        the results will be written
  --influxlog INFLUXLOG
                        Log to InfluxDB; IP/Url of of the InfluxDB-Server where
                        the results will be written
```

## Examples

Query single register, where 192.168.0.48 is the IP of your SMA inverter
```sh
$ python main.py -a"192.168.0.48" 30775

30775 GridMs.TotW (Leistung) 1.23 kW
```

Query single register, ervery 60 seconds (daemon)
```sh
$ python main.py -a"192.168.0.48" -d 30775 

30775 GridMs.TotW (Leistung) 1.23 kW
30775 GridMs.TotW (Leistung) 2.34 kW
30775 GridMs.TotW (Leistung) 3.45 kW
...
```

Query all registers
```sh
$ python main.py -a"192.168.0.48" -all

```

Query registers defined in a file
```sh
$ python main.py -a"192.168.0.48"  -f"registers.txt" 

```

Generate openhab items for registers defined in a file
```sh
$ python main.py -a"192.168.0.48"  -f"registers.txt" -ohitems

 //  AC-Seite
Number SMA_Metering_TotWhOut "Gesamtertrag [%.0f Wh]" <none> (SMA)
Number SMA_Metering_DyWhOut "Tagesertrag [%.0f Wh]" <none> (SMA)
String SMA_Metering_TotOpTms "Betriebszeit [%s]" <none> (SMA)
String SMA_Metering_TotFeedTms "Einspeisezeit [%s]" <none> (SMA)
Number SMA_Operation_GriSwCnt "Anzahl Netzzuschaltungen [%.0f ]" <none> (SMA)
Number SMA_GridMs_TotW "Leistung [%.0f W]" <none> (SMA)
Number SMA_GridMs_W_phsA "Leistung L1 [%.0f W]" <none> (SMA)
Number SMA_GridMs_W_phsB "Leistung L2 [%.0f W]" <none> (SMA)
Number SMA_GridMs_W_phsC "Leistung L3 [%.0f W]" <none> (SMA)
Number SMA_GridMs_PhV_phsA "Netzspannung Phase L1 [%.2f V]" <none> (SMA)
Number SMA_GridMs_PhV_phsB "Netzspannung Phase L2 [%.2f V]" <none> (SMA)
Number SMA_GridMs_PhV_phsC "Netzspannung Phase L3 [%.2f V]" <none> (SMA)
Number SMA_GridMs_TotA "Netzstrom [%.3f A]" <none> (SMA)
Number SMA_GridMs_Hz "Netzfrequenz [%.2f Hz]" <none> (SMA)
Number SMA_GridMs_TotVAr "Blindleistung [%.0f VAr]" <none> (SMA)
Number SMA_GridMs_VAr_phsA "Blindleistung L1 [%.0f VAr]" <none> (SMA)
Number SMA_GridMs_VAr_phsB "Blindleistung L2 [%.0f VAr]" <none> (SMA)
Number SMA_GridMs_VAr_phsC "Blindleistung L3 [%.0f VAr]" <none> (SMA)
Number SMA_GridMs_TotVA "Scheinleistung [%.0f VA]" <none> (SMA)
Number SMA_GridMs_VA_phsA "Scheinleistung L1 [%.0f VA]" <none> (SMA)
Number SMA_GridMs_VA_phsB "Scheinleistung L2 [%.0f VA]" <none> (SMA)
Number SMA_GridMs_VA_phsC "Scheinleistung L3 [%.0f VA]" <none> (SMA)
Number SMA_GridMs_A_phsA "Netzstrom Phase L1 [%.3f A]" <none> (SMA)
Number SMA_GridMs_A_phsB "Netzstrom Phase L2 [%.3f A]" <none> (SMA)
Number SMA_GridMs_A_phsC "Netzstrom Phase L3 [%.3f A]" <none> (SMA)

 //  DC-Seite
Number SMA_Isolation_LeakRis "Isolationswiderstand [%.0f Ohm]" <none> (SMA)
Number SMA_DcMs_Amp_MPPT1 "DC Strom Eingang MPPT1 [%.3f A]" <none> (SMA)
Number SMA_DcMs_Vol_MPPT1 "DC Spannung Eingang  MPPT1 [%.2f V]" <none> (SMA)
Number SMA_DcMs_Watt_MPPT1 "DC Leistung Eingang  MPPT1 [%.0f W]" <none> (SMA)
Number SMA_DcMs_Amp_MPPT2 "DC Strom Eingang MPPT2 [%.3f A]" <none> (SMA)
Number SMA_DcMs_Vol_MPPT2 "DC Spannung Eingang MPPT2 [%.2f V]" <none> (SMA)
Number SMA_DcMs_Watt_MPPT2 "DC Leistung Eingang  MPPT2 [%.0f W]" <none> (SMA)
Number SMA_Inverter_DclVol "Zwischenkreisspannung [%.2f V]" <none> (SMA)
Number SMA_Isolation_FltA "Fehlerstrom [%.3f A]" <none> (SMA)
Number SMA_DcMs_Amp__1 "DC Strom Eingang ?1 [%.3f A]" <none> (SMA)
Number SMA_DcMs_Am__2 "DC Strom Eingang ?2 [%.3f A]" <none> (SMA)

 //  Status
String SMA_DtTm_Tm "Systemzeit [%s]" <none> (SMA)
String SMA_Operation_Health "Zustand [%s]" <none> (SMA)
String SMA_Operation_Evt_Prio "Empfohlene Aktion [%s]" <none> (SMA)
String SMA_Operation_Evt_Msg "Meldung [%s]" <none> (SMA)
String SMA_Operation_Evt_Dsc "Fehlerbehebungsmaßnahme [%s]" <none> (SMA)
Number SMA_Operation_Evt_EvtNo "Aktuelle Ereignisnummer für Hersteller [%.0f ]" <none> (SMA)
String SMA_Operation_PvGriConn "Netzanbindung der PV-Anlage  [%s]" <none> (SMA)
Number SMA_Coolsys_Cab_TmpVal "Innentemperatur [%.1f °C]" <none> (SMA)
String SMA_Operation_OpStt "Betriebsstatus [%s]" <none> (SMA)

```

Query registers defined in a file, and send it to InfluxDB (or other REST web service, if you modify the *openhablogger* or *influxlogger*)
```sh
$ python3 main.py -a"192.168.0.48"  -f"registers_influx.txt" --influxlog "192.168.0.200" --logport 8086 -d
```
