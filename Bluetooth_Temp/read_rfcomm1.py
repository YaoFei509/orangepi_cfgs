#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 
#  Send a 't' and receive 2 lines
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

# repeat 5 times to read from rfcomm
t = 0
SER = serial.Serial(PORT, 9600)

while (t<10):
    try:
        SER.write(b'n')
        num = int(SER.readline())
        SER.write(b't')

        line1 = SER.readline().decode('ascii').split()
        if num == 2:
            line2 = SER.readline().decode('ascii').split()

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
    val = (tnow, str(line1[1]), str(line1[0]))
    cursor.execute(ISQL, val)
    print ( num, line1[1])

    if num == 2 :
        val = (tnow, str(line2[1]), str(line2[0]))
        cursor.execute(ISQL, val)
        print ( line2[1])

    cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

cursor.close()
cnx.close()
