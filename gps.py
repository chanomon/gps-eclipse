#!/usr/bin/env python3

from gps3 import gps3
import time
#import json

gnssid_mapping = {
    0: 'GPS',
    1: 'SBAS',
    2: 'Galileo',
    3: 'BeiDou',
    4: 'IMES',
    5: 'QZSS',
    6: 'GLONASS',
    7: 'NavIC'
}

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()

gps_socket.connect(host="127.0.0.1", port=2947)
gps_socket.watch()

try:
    for new_data in gps_socket:
        if new_data:

            data_stream.unpack(new_data)
            satellites_info = data_stream.SKY.get('satellites', [])
            time_ = data_stream.TPV.get('time', 'N/A')
            lat = data_stream.TPV.get('lat', 'N/A')
            lon = data_stream.TPV.get('lon', 'N/A')
            alt = data_stream.TPV.get('alt', 'N/A')
            print(f"------TPV DATA------\nTime: {time_}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")
            
            
            if type(satellites_info) is list:#else is a str and has no info
                print("------SATELLITES DATA------")
                for satellite in satellites_info:
                    gnssid = satellite.get('gnssid', 'N/A')
                    constellation = gnssid_mapping.get(gnssid, 'UNKOWN')
                    elevation = satellite.get('el', 'N/A')
                    azimuth = satellite.get('az', 'N/A')
                    snr = satellite.get('ss', 'N/A')
                    used = satellite.get('used', False)
                    print(f"Constellation: {constellation}, Elevation: {elevation}, Azimuth: {azimuth}, SNR: {snr}, Used: {used}")
            #time.sleep(1)
            # else:
            #     print('Esperando una fijación 2D o 3D...')

except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    gps_socket.close()