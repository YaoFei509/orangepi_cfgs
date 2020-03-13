#!/usr/bin/python3

#
# Read MAX6675 from SPI interface and send to database
#

import mysql.connector
import sys
import time
import spidev

spi = spidev.SpiDev()  # for One, 0.0, for Zero: 1,0
spi.open(0,0)          # for One, 0.0, for Zero: 1,0

# Read 5 times, and use average value
temp = 0;
for i in range(5):
    resp = spi.readbytes(2)
    temp += ((resp[1] + resp[0]*256) & 0x7ff8)
    time.sleep(0.01)

spi.close
temp /= 160 ; # /8/5*0.25 

# Insert to database
user = 'www'
pwd  = 'www'
host = 'yfhomeserver.local'
db   = 'yfhome'

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()
isql = "INSERT home_temp VALUES "    

try:
    tnow = int(time.time())   
    sql = isql + "(0, {}, 0, {:.2f}, '28-KTHERFISH')".format(tnow, temp)
# for DEBUG only     
#    print(sql)
        
    cursor.execute(sql)

except mysql.connector.Error as err:
    print("insert table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

cnx.commit()
cursor.close()
cnx.close()
