#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 

import mysql.connector
import sys
import time
import serial

PORT = "/dev/rfcomm0"

USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

SQL  = "INSERT INTO home_temp VALUES (0, %s, %s, %s, %s )"

cnx = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
cursor = cnx.cursor()

while True:
    print ("Open:")
    try :
        s = serial.Serial(PORT, 9600)
        line1 = s.readline()

    except serial.serialutil.SerialException :
           continue
    else :
        break

print ("Connected")
    
while True:
    try :
        # Now time
        tnow = int(time.time())   
        line1 = s.readline().decode('ascii').split()

    except serial.serialutil.SerialException:
        print ("RFCOMM fail")
        break

    # per minute
    if (tnow % 60) > 0 :
        continue

    try:
        val = (tnow, str(line1[0]), float(line1[1]), str(line1[2]))
        print(val)
        cursor.execute(SQL, val)
        cnx.commit()

    except mysql.connector.Error as err:
        print("insert table 'home_temp' failed.")
        print("Error: {}".format(err.msg))
        break 

s.close
cursor.close()
cnx.close()
