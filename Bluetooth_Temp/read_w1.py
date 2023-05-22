#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
import mysql.connector
import sys, os
import time

USER = 'www'
PWD  = 'www'
DB   = 'yfhome'
SQL = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s) "

HOSTLIST  = ['192.168.20.20', 'yfhomeserver.local', 'yfserver.dynv6.net']

for h in HOSTLIST:
    if os.system("ping -c 1 -w2 " + h + " > /dev/null 2>&1") == 0: 
        HOST = h
        break

try:
    cnx = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
    cursor = cnx.cursor()

    tnow = int(time.time())   
    for sensor in W1ThermSensor.get_available_sensors():
        ssum = 0.0
        for i in range(3):
            stemp = sensor.get_temperature()
            ssum += stemp
        ssum /= 3
        val = (tnow, format(ssum, "0.1f"), "28"+sensor.id)
        #print(val)

        cursor.execute(SQL, val)
        cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

cursor.close()
cnx.close()
