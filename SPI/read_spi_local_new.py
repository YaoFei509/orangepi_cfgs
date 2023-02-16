#!/usr/bin/python3

#
# Read MAX 31855 from SPI interface and send to database
#
# pip3 install spidev pyMax31855
#

import time
import mysql.connector
from max31855 import max31855

SQL  = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s )"


while True:
    obj_ = max31855(bus=0,device=0)

    tmax = -20000
    tmin = 20000
    temp = 0 

    for i in range(7):
        while True:
            ret = obj_.read_value()
            if ret['fault'] == None :
                break;

        t = ret['t_tc_lin']
        temp += t;
        if t > tmax :
            tmax = t

        if t < tmin :
            tmin = t

        time.sleep(0.5)

    temp -= tmax
    temp -= tmin
    temp /= 5

    print('T:', temp, '\t', tmax, '\t', tmin)
    time.sleep(5)

