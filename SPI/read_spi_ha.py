#!/usr/bin/python3

#
# Read MAX 31855 from SPI interface and send to stdout
#
# pip3 install spidev pyMax31855
#

import time
from max31855 import max31855

# Read from MAX31855
obj_ = max31855(bus=0,device=0)

tmax = -20000
tmin = 20000
temp = 0 

# Read 7 times, remove the Max and the Min, and use average value
for i in range(7):
    while True:
        ret = obj_.read_value()
        # Skip failure 
        if ret['fault'] == None :
            break;
        else :
            time.sleep(0.1)

    t = ret['t_tc_lin']
    temp += t;
    if t > tmax :
        tmax = t

    if t < tmin :
        tmin = t

    time.sleep(0.25)

temp -= tmax
temp -= tmin
temp /= 5

print(temp)
