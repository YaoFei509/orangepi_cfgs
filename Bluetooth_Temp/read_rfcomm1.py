#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 
#  Send a 't' and receive 2 lines
#

import sys
import time
import serial
import mysql.connector

if sys.argv[1]:
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
        SER.write(b't')
        line1 = SER.readline().decode('ascii').split()
        line2 = SER.readline().decode('ascii').split()

    except serial.serialutil.SerialException:
        t += 1

    else:
        break

SER.close()

if t==10:
    print("RFCOMM fail")
    sys.exit()

cnx = mysql.connector.connect(USER, PWD, HOST, DB)
cursor = cnx.cursor()
ISQL = "INSERT home_temp VALUES "    

try:
    sql = ISQL + "(0, {}, 0, {}, '{}')".format(tnow, str(line1[1]), str(line1[0])) \
        + ",(0, {}, 0, {}, '{}')".format(tnow, line2[1], line2[0])
    print(sql)
        
    cursor.execute(sql)
    cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

cursor.close()
cnx.close()
