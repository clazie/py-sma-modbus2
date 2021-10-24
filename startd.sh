#!/bin/sh

cd `dirname $0`
python3 main.py -a"192.168.0.48"  -f"registers.txt" -o"localhost" -d
