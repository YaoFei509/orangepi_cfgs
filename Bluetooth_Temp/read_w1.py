#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
import mysql.connector
import sys, os
import time

user = 'www'
pwd  = 'www'
host = 'yfhomeserver.local'
db   = 'yfhome'

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()
SQL = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s) "

try:
    tnow = int(time.time())   
    for sensor in W1ThermSensor.get_available_sensors():
        ssum = 0.0
        for i in range(3):
            stemp = sensor.get_temperature()
            ssum += stemp
        ssum /= 3
        val = (tnow, ssum, "28"+sensor.id)
        print(val)
        
        cursor.execute(SQL, val)
        cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

cursor.close()
cnx.close()
