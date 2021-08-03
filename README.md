# orangepi_cfgs
My OrangePi One/Zero toys
================================

# SPI 
use the SPI interface of OrangePi One/Zero to attach a MAX6675 thermcouple.

The MAX6675 connects to OPi One as:

|MAX6675| One GPIO |
| :-: | :-: | 
|VCC| PIN17 |
|GND| PIN20 |
|SCK| PIN23 |
|CS | PIN24 |
|SO | PIN21 |

need spidev module 

`pip3 install spidev`

But it is very very noisely, don't use.
测量数据噪音太大了，没有任何实际用处。

# GPS
连接一个GPS模块做NTP授时服务器。

use GPS module connected to UART, read GPS time and feed to NTP as a Time base.
need a GPIO PIN to receive GPS PPS pulse.

I use gpsd to receive GPS data, so must setup the actual UART port in /etc/default/gpsd.
GPSD will send the GPS timestamp to ntpd by SHMEM, so setup the /etc/ntp.conf

maybe need fix the /lib/systemd/system/gpsd.socket to allow network remote access GPS data:

`ListenStream=0.0.0.0:2947`

# Bluetooth_Temp
use a DS18B20 connected to 1-Wire i/f, and my remote ds18b20 linked by bluetooth

早期方案，DS18B20连接在一个单片机上，单片机再用蓝牙模块把数据发送到OrangePi One 上，用这里的perl脚本送服务器。
单片机和蓝牙的可靠性太低了，反正家里好几个闲置的OrangePi Zero，就把DS18B20接到Zero的GPIO上，用Python脚本读并送入数据库。
owserver还能把DS18B20远程接入到HomeAssistant
这里几个perl脚本就只有存档价值了。
