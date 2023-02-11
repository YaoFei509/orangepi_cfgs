#!/usr/bin/python3

#
# Read MAX 31855 from SPI interface and send to database
#
# pip3 install spidev pyMax31855
#

import time
import mysql.connector
from max31855 import max31855

# Insert to database
USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

SQL  = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s )"

obj_ = max31855(bus=0,device=0)

while True:
    ret = obj_.read_value()
    if ret['fault'] == None :
        break;

temp = ret['t_tc_lin']

try:
    tnow = int(time.time())
    val  = (tnow, float(temp), '28-KTHERFISH')

    CNX = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
    CURSOR = CNX.cursor()
    CURSOR.execute(SQL, val)
    CNX.commit()
    print(val)

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

CURSOR.close()
CNX.close()
