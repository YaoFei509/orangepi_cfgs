#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 

import mysql.connector
import sys
import time
import serial

PORT = "/dev/rfcomm0"

user = 'www'
pwd  = 'www'
host = 'yfhomeserver.local'
db   = 'yfhome'

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
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
    # repeat 10 times to read from rfcomm
    t = 0
    while (t<10):
        try :
            # Now time
            tnow = int(time.time())   
            line1 = s.readline().decode('ascii').split()

        except serial.serialutil.SerialException:
            t += 1

        else :
            break

    if (t == 10) :
        print ("RFCOMM fail")
        break

    # per minute
    if (tnow % 60) > 0 :
        continue

    try:
        sql = "INSERT home_temp VALUES (0, {}, '{}', {}, '{}')".format(tnow, str(line1[0]), str(line1[1]), str(line1[2]))
        print(sql)
        cursor.execute(sql)

    except mysql.connector.Error as err:
        print("insert table 'mytable' failed.")
        print("Error: {}".format(err.msg))
        break 
    else:
        cnx.commit

s.close
cursor.close()
cnx.close()
