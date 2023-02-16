#!/usr/bin/python3

#
# Read MAX 31855 from SPI interface and send to database
#
# pip3 install spidev pyMax31855
#

import time
import mysql.connector
from max31855 import max31855
#
PROBE  = "28-KTHERFISH"
#PROBE = "28-KTHERAIR"
#PROBE = "28-KTHERMONE"

# Insert to database
USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

SQL  = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s )"

# Read from MAX31855
obj_ = max31855(bus=0,device=0)

tmax = -20000
tmin = 20000
temp = 0 

# Read 7 times, remove the Max and the Min, and use average value
for i in range(7):
    while True:
        ret = obj_.read_value()
        # Skip failure 
        if ret['fault'] == None :
            break;
        else :
            time.sleep(0.1)

    t = ret['t_tc_lin']
    temp += t;
    if t > tmax :
        tmax = t

    if t < tmin :
        tmin = t

    time.sleep(0.5)

temp -= tmax
temp -= tmin
temp /= 5

try:
    tnow = int(time.time())
    val  = (tnow, float(temp), PROBE)

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