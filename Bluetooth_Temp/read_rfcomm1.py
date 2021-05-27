#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 
#  Send a 'n' to get numbers of 18B20
#  Send a 't' and receive lines
#

import sys
import time
import serial
import mysql.connector

if len(sys.argv) > 1:
    PORT = sys.argv[1]
else:
    PORT = "/dev/rfcomm1"

USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

# Now time
tnow = int(time.time())

# repeat 10 times to read from rfcomm
t = 0
tt  = [[0] * 5] * 2 
mac = [''] * 2 

SER = serial.Serial(PORT, 9600)

while (t<10):
    try:
        SER.write(b'n')
        num = int(SER.readline())

        for i in range(5) :
            SER.write(b't')

            for j in range(num) :
                line = SER.readline().decode('ascii').split()
                mac[j] = line[0]
                tt[j][i] = float(line[1])

    except serial.serialutil.SerialException:
        t += 1

    else:
        break

SER.close()

if t==10:
    print("RFCOMM fail")
    sys.exit()

cnx = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
cursor = cnx.cursor()
ISQL = "INSERT home_temp VALUES (0, %s, 0, %s, %s) "    

try:
    for i in range(num):
        tsum = (sum(tt[j]) - max(tt[j]) - min(tt[j]) ) / 3
        val = (tnow, str(tsum), str(mac[j]))
        cursor.execute(ISQL, val)
        print ( num, tsum)

    cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

cursor.close()
cnx.close()
