#!/usr/bin/python3

#
# Read MAX 31855 or MAX6675 from SPI interface and send to database
#
import time
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
    bus.max_speed_hz = 1000000
    resp = bus.readbytes(4)

    t = (resp[0] << 24) | (resp[1] << 16) | (resp[2] << 8) | resp[3]

    #Internal code-juncton
    internal = (t >> 4) & 0x7ff
    if t & 0x800:
        internal = internal - 4096
    internal *= 0.0625

    if t & 0x7:
        temp = float('NaN')
        print("Sensor error:  {}".format(resp[3] & 7))

    if t&0x80000000:
        temp = t >> 18
        temp = temp - 16384
    else:
        temp = t >> 18

    temp *= 0.25
    return temp

SPI = spidev.SpiDev()
SPI.open(0,0)
temp = read_max31855(SPI)
SPI.close()

tnow = int(time.time())
print(tnow, float(temp))
