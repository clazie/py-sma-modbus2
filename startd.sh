#!/bin/bash

cd `dirname $0`
source run/bin/activate
python3 main.py -a"192.168.0.48"  -f"registers_influx.txt" --influxlog "192.168.0.200" --logport 8086 -d
