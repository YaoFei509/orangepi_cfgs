# orangepi_cfgs
My OrangePi One/Zero toys
================================

# SPI 
use the SPI interface of OrangePi One/Zero to attach a MAX6675 thermcouple.

 the MAX6675 connects to OPi One as:

|MAX6675| One GPIO |
| :-: | :-: | 
|VCC| PIN17 |
|GND| PIN20 |
|SCK| PIN23 |
|CS | PIN24 |
|SO | PIN21 |

need spidev module 

`pip3 install spidev`

# GPS
use GPS module connected to UART, read GPS time and feed to NTP as a Time base.
need a GPIO PIN to receive GPS PPS pulse.

I use gpsd to receive GPS data, so must setup the actual UART port in /etc/default/gpsd.
GPSD will send the GPS timestamp to ntpd by SHMEM, so setup the /etc/ntp.conf

maybe need fix the /lib/systemd/system/gpsd.socket to allow network remote access GPS data:

`ListenStream=0.0.0.0:2947`



# Bluetooth_Temp
use a DS18B20 connected to 1-Wire i/f, and my remote ds18b20 linked by bluetooth
