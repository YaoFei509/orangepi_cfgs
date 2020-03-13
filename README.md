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

# Bluetooth_Temp
use a DS18B20 connected to 1-Wire i/f, and my remote ds18b20 linked by bluetooth
