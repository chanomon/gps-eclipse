# gps-eclipse
A distributed system to read and save gps data in a server for the 2024 eclipse.
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
Get sure you have your gps receptor connected to your system.

Configure gpsd:

**Ubuntu**
```
sudo nano /etc/default/gpsd
```

**Fedora**
```
sudo nano /etc/sysconfig/gpsd
```

**Arch Linux**
```
sudo nano /etc/conf.d/gpsd

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
or this
```
cgps
```
This will display an gps interface showing the gps recordings, something like this:
![image](https://github.com/chanomon/gps-eclipse/assets/19211938/89797f05-85ee-467d-8380-d52327799141)

or in cgps case, this:

![image](https://github.com/chanomon/gps-eclipse/assets/19211938/2458db41-780e-4e34-90ab-5b779c793c4c)


To stop gpsmon or cgps use Ctr-c

Also, to see gpsd status, use:
```
sudo service gpsd status
```


**Note**
Make sure you have the correct permissions to read/write with the gps device:
```
sudo usermod -aG dialout $USER
```
To stop gpsd service:
```
#for systems that use Systemd:
sudo systemctl stop gpsd
#for systems that use init.d:
sudo service gpsd stop
```
## GPDS request/response protocol:
[https://gpsd.gitlab.io/gpsd/gpsd_json.html](https://gpsd.gitlab.io/gpsd/gpsd_json.html)

## GPSRINEX
Use gpsrinex to produce RINEX files from the GPS data. Use the command:
```
gpsrinex -i 30 -n 2 localhost:2947:/dev/gps0 # check the path of your gps device, in this case is /dev/gps0
```
Use ```gpsrinex -h``` to print usage message.

Here you can find more documentation of gps rinex: [https://gpsd.gitlab.io/gpsd/gpsrinex.html](https://gpsd.gitlab.io/gpsd/gpsrinex.html)

## Getting gps data with python
Run one of the python codes included in this repo, get sure you have installed gps3 or gpsd-py3 library.
If not, you can do this with:
```
pip3 install --upgrade gps3 gpsd-py3
```
Finally run 
```
python gps.py
#or alternativelly 
python gps2.py
```
