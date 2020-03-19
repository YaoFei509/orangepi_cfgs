#!/usr/bin/python3

#
# Read MAX6675 from SPI interface and send to database
#
import sys
import time
import spidev
import mysql.connector

SPI = spidev.SpiDev()  # for One, 0.0, for Zero: 1,0
SPI.open(0, 0)          # for One, 0.0, for Zero: 1,0

# Read 5 times, and use average value
temp = 0
for i in range(5):
    resp = SPI.readbytes(2)
    temp += ((resp[1] + resp[0]*256) & 0x7ff8)
    time.sleep(0.2)   # min 0.18s

SPI.close()
temp /= 160 # /8/5*0.25 

# Insert to database
USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

SQL  = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s )"

cnx = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
cursor = cnx.cursor()

try:
    tnow = int(time.time())
    val  = (tnow, float(temp), '28-KTHERFISH')
    cursor.execute(SQL, val)
    cnx.commit()
    #print (val)

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

cursor.close()
cnx.close()
