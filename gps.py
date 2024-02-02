#import gpsd
#import time
#
## Connect somewhere else
#gpsd.connect(host="127.0.0.1", port=2947)
#while True:
#    packet = gpsd.get_current()
#    if packet.mode >= 2:
#        break
#    print("Esperando una fijación 2D...")
#    time.sleep(1)
#
#print("Latitude: ", packet.lat)
#print("Longitude: ", packet.lon)
#print("Altitude: ", packet.alt)
from gps3 import gps3

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()

gps_socket.connect(host="127.0.0.1", port=2947)
gps_socket.watch()

try:
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
	    satellites_info = data_stream.TPV.get('satellites', [])

	    time = data_stream.TPV.get('time', 'N/A')
	    lat = data_stream.TPV.get('lat', 'N/A')
	    lon = data_stream.TPV.get('lon', 'N/A')
	    alt = data_stream.TPV.get('alt', 'N/A')
    
	    print(f"Time: {time}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")
		
	    for satellite in satellites_info:
	        prn = satellite.get('PRN', 'N/A')
		elevation = satellite.get('el', 'N/A')
		azimuth = satellite.get('az', 'N/A')
		snr = satellite.get('ss', 'N/A')
		used = satellite.get('used', False)
		
		print(f"Sat PRN: {prn},  Elevation: {elevation}, Azimuth: {azimuth}, SNR: {snr}, Used: {used}")
		
		                
            #else:
            #    print('Esperando una fijación 2D o 3D...')

            
except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    gps_socket.close()
