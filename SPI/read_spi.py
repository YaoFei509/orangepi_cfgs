#!/usr/bin/python3

#
# Read MAX 31855 or MAX6675 from SPI interface and send to database
#
import time
import mysql.connector
import spidev

# Read from MAX6675
def read_max6675(bus):
    # Read 5 times, and use average value
    temp = 0
    for i in range(5):
        resp = bus.readbytes(2)
        temp += (resp[1] + resp[0] << 8) & 0x7ff8
        time.sleep(0.2)   # min 0.18s

    temp /= 160 # /8/5*0.25
    return temp

def read_max31855(bus):
    resp = bus.readbytes(4)

    t = (resp[0] << 24) | (resp[1] << 16) | (resp[2] << 8) | resp[3]

    #Internal code-juncton
    internal = (t >> 4) & 0x7ff
    if t & 0x800:
        internal = internal - 4096
    internal *= 0.0625

    if t&0x80000000:
        temp = t >> 18
        temp = temp - 16384
    else:
        temp = t >> 18

    temp *= 0.25

    if t & 0x7:
        temp = float('NaN')
        print("Sensor error:  {}".format(resp[3] & 7))

    return temp

# Insert to database
USER = 'www'
PWD  = 'www'
HOST = 'yfhomeserver.local'
DB   = 'yfhome'

tt = [0]*7

SQL  = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s )"

CNX = mysql.connector.connect(user=USER, password=PWD, host=HOST, database=DB)
CURSOR = CNX.cursor()

SPI = spidev.SpiDev()
SPI.open(0,0)
SPI.max_speed_hz = 200000

while True :
      temp  = read_max31855(SPI)
      if temp != float('NaN') :
            break;

SPI.close()

try:
    tnow = int(time.time())
    val  = (tnow, float(temp), '28-KTHERFISH')
    print(val)
    CURSOR.execute(SQL, val)
    CNX.commit()

except mysql.connector.Error as err:
    print("insert table 'home_temp' failed.")
    print("Error: {}".format(err.msg))

CURSOR.close()
CNX.close()
