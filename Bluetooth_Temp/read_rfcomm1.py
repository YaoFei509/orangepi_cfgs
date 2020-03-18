#!/usr/bin/python3

# Read 18B20 from Bluetooth
# 
#  Send a 't' and receive 2 lines
#

import mysql.connector
import sys
import time
import serial

PORT = "/dev/rfcomm1"

user = 'www'
pwd  = 'www'
host = 'yfhomeserver.local'
db   = 'yfhome'

# Now time
tnow = int(time.time())   

# repeat 5 times to read from rfcomm
t = 0
s = serial.Serial(PORT, 9600)
while (t<10):
    try:
        s.write(b't')
        line1 = s.readline().decode('ascii').split()
        line2 = s.readline().decode('ascii').split()

    except serial.serialutil.SerialException:
        t += 1

    else:
        break

s.close

if (t==10) :
    print ("RFCOMM fail")
    sys.exit()

#print(line1)

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()
isql = "INSERT home_temp VALUES "    

try:
    sql = isql + "(0, {}, 0, {}, '{}')".format(tnow, str(line1[1]), str(line1[0])) + ",(0, {}, 0, {}, '{}')".format(tnow, line2[1], line2[0])
    print(sql)
        
    cursor.execute(sql)
    cnx.commit()

except mysql.connector.Error as err:
    print("insert table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

cursor.close()
cnx.close()
