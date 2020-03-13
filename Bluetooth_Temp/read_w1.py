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
isql = "INSERT home_temp VALUES "    

try:
    tnow = int(time.time())   
    for sensor in W1ThermSensor.get_available_sensors():
        ssum = 0.0
        for i in range(3):
            stemp = sensor.get_temperature()
            ssum += stemp
        ssum /= 3
        sql = isql + "(0, {}, 0, {:.2f}, '28{}')".format(tnow, ssum, sensor.id)
        print(sql)
        
        cursor.execute(sql)

except mysql.connector.Error as err:
    print("insert table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()


cnx.commit()
cursor.close()
cnx.close()
