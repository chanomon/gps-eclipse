#!/usr/bin/env python3

from gps3 import gps3
import time
import json
from datetime import datetime

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

PATH = '/tmp/send-gps-data/'
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()

gps_socket.connect(host="127.0.0.1", port=2947)
gps_socket.watch()

end_time = time.time() + 60

try:
    records = [] 
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            satellites_info = data_stream.SKY.get('satellites', [])
            if type(satellites_info) is list:
                satellite_records = []  # Lista para almacenar registros de satélites
                for satellite in satellites_info:
                    gnssid = satellite.get('gnssid', 'N/A')
                    constellation = gnssid_mapping.get(gnssid, 'UNKOWN')
                    elevation = satellite.get('el', 'N/A')
                    azimuth = satellite.get('az', 'N/A')
                    snr = satellite.get('ss', 'N/A')
                    used = satellite.get('used', False)
                    satellite_record = {
                        'Constellation': constellation,
                        'Elevation': elevation,
                        'Azimuth': azimuth,
                        'SNR': snr,
                        'Used': used
                    }
                    satellite_records.append(satellite_record)
                time_ = data_stream.TPV.get('time', 'N/A')
                lat = data_stream.TPV.get('lat', 'N/A')
                lon = data_stream.TPV.get('lon', 'N/A')
                alt = data_stream.TPV.get('alt', 'N/A')
                ###################################################
                ######## Saving receiver data and Satellites data.
                ###################################################
                record = {
                    'Time': time_,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Altitude': alt,
                    'Satellites': satellite_records
                }
                records.append(record)
                print(f"------TPV DATA------\nTime: {time_}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")
        if time.time() > end_time:#save as json
            first_time = records[0]['Time']
            timestamp = datetime.strptime(first_time, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'gps_records_{timestamp}.json'
            with open(PATH+filename, 'w') as file:
                json.dump(records, file, indent=2)
            #start_time = time.time()
            end_time = end_time + 60
            records = []
            print('######################################\n'
                     '####------SAVED 1 MIN RECORD------####\n'
                     '######################################')
except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    gps_socket.close()
