# gps-eclipse
A distributed system to read and save gps data in a server for the 2024 eclipse.
We'll use gpsd, this is a service daemon that monitors one or more GPSes or AIS receivers attached to a host computer through serial or USB ports, making all data on the location/course/velocity of the sensors available to be queried on TCP port 2947 of the host computer.
Then we will send the data with SCP to a remote server and save them in directories accordongly to date name of the files.

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
gpsrinex -i 30 -n 30 localhost:2947:/dev/gps0 # check the path of your gps device, in this case is /dev/gps0
```
Use ```gpsrinex -h``` to print usage message.

Here you can find more documentation of gps rinex: [https://gpsd.gitlab.io/gpsd/gpsrinex.html](https://gpsd.gitlab.io/gpsd/gpsrinex.html)

Once the proces ends, you could get a file of observation like this:

![image](https://github.com/chanomon/gps-eclipse/assets/19211938/35ae3b1e-f98a-4866-8ced-89a4272b6dfa)




## Getting gps data with python and moving data to remote server.
With this codes we will record gps data and send them via SCP to a remote server. 

To do this, first we will share a rsa key to move the files via SCP without writing the password.
In terminal, type:
```
ssh-keygen
```
With this command you''ll obtain two files: *id_rsa.pub* (public key) and *id_rsa* (private key)
Send the public key to the remote server to make scp/ssh connections witohut password:
```
ssh-copy-id user@remote_server:/path_to_save/id_rsa.pub
```

Now you need to install a local crontab comand.
To do this, copy the content in *localcrontab* file.
Then run this comand:
```
crontab -e
```
If it's your first time with crontab, you'll need to select a text editor.
Then at the last line of the file, paste the content of *localcrontab*
Make sure you have the right user, ip adress of the remote server and the correct paths.
Press enter to add a new line in the file and save it.

Simimlarlly make the same processes in the remote server, this time copy the content in *remoteserver/remotecrontab* and paste it in the crontab file after using
```
crontab -e
```


In the system where you have the gps system, run one of the python codes included in this repo, get sure you have installed gps3 or gpsd-py3 library.
If not, you can do this with:
``` 
pip3 install --upgrade gps3 gpsd-py3
```

Finally run 
```
python gps--3.py
#or alternativelly 
python gps2.py
```


## Plotting the data
In the remote server you can plot the data with *remoteserver/plot.py*
First check you have the correct location path of the files.
Run: 
```
python remoteserver/plot.py
```
The prompt will ask for the path of the files, write it and then press enter.
You should get a plot like this:
![Image](https://github.com/chanomon/gps-eclipse/blob/main/plot.png)

## Saving binary data from gpsd:
```
gpspipe -x 900 -R localhost:2947:/dev/gps0 > outfile.ubx
```
the number after "-x" indicates de number of seconds for recording.

## Convert binary file to rinex file:
Having previously installed RTKLIB, use the comand:
```
convbin -f 1 outfile.ubx -o rinexfile.obs
```
voila,  you should now have a rinex file.
