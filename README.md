# gps-eclipse
A distributed system to read and save gps data in a server for the 2024 eclipse
We'll use gpsd, this is a service daemon that monitors one or more GPSes or AIS receivers attached to a host computer through serial or USB ports, making all data on the location/course/velocity of the sensors available to be queried on TCP port 2947 of the host computer.

## Installation
You need to install gpsd, an aplication for GNU/linux. 

**Ubuntu**:
```
sudo apt-get update
sudo apt-get install gpsd gpsd-clients
```
**Fedora**:
```
sudo dnf install gpsd gpsd-clients
```
**Arch Linux**:
```
sudo pacman -S gpsd gpsd-clients
```
Configure gpsd:

**Ubuntu**
```
sudo nano /etc/default/gpsd
```

Edit the file like this:
```
# Make sure this configuration is done accordingly to your needs
START_DAEMON="true"
GPSD_OPTIONS="-n -G"
DEVICES="/dev/ttyUSB0"  # Change this acordingly to your GPS device
```
To initiate gpsd:
```
sudo service gpsd start  # For systems that use Systemd
# or
sudo /etc/init.d/gpsd start  # For systems that use init.d
```

Check conection, in terminal write:
```
gpsmon
```
This will display an gps interface showing the gps recordings, something like this:
![image](https://github.com/chanomon/gps-eclipse/assets/19211938/89797f05-85ee-467d-8380-d52327799141)

To stop gpsmon use Ctr-c

**Note**
Make sure you have the correct permissions to read/write with the gps device:
```
sudo usermod -aG dialout $USER
```
To stop gpsd:
```
#for systems that use Systemd:
sudo systemctl stop gpsd
#for systems that use init.d:
sudo service gpsd stop
```
