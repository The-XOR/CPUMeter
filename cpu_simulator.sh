#!/bin/bash

CPU=100

stty -F /dev/ttyACM0 raw -echo
while true; do
    CPU=$((CPU + 10))
    if [ $CPU -gt 100 ]; then
        CPU=0
    fi
    echo "Carico CPU: $CPU%"
    cpuHex=$(printf "%02X" $CPU)
    echo -n -e \x$cpuHex > /dev/ttyACM0
    sleep 2
done
