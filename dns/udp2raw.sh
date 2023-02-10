#!/bin/bash

# for udp2raw

#udp2raw
# ARMv7 32bit
#nohup /usr/local/bin/udp2raw_arm_asm_aes --conf-file /usr/local/etc/udp2raw.conf > /var/log/udp2raw.log 2>&1 & echo $! > /var/run/udp2raw.pid

# ARMv8 64bit
nohup /usr/local/bin/udp2raw_arm64_asm_aes --conf-file /usr/local/etc/udp2raw.conf > /var/log/udp2raw.log 2>&1 & echo $! > /var/run/udp2raw.pid

# x86 64bit
#nohup /usr/local/bin/udp2raw_amd_hw_aes --conf-file /usr/local/etc/udp2raw.conf > /var/log/udp2raw.log 2>&1 & echo $! > /var/run/udp2raw.pid

sleep 3 

chmod a+w /tmp/udp2raw.fifo
