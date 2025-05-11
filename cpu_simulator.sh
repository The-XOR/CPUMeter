#!/bin/bash

CPU=10

stty -F /dev/ttyACM0 raw -echo
while true; do
    CPU=$((CPU + 10))
    if [ $CPU -gt 100 ]; then
        CPU=0
        echo "Simulazione timeout"
        sleep 12
    fi
    echo "Carico CPU: $CPU%"
    cpuHex=$(printf "%02X" $CPU)
    cpuHex="\x"$cpuHex""
    echo -n -e $cpuHex > /dev/ttyACM0
    sleep 2
done
