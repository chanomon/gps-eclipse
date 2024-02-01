#import gpsd
#import time
#
## Connect somewhere else
#gpsd.connect(host="127.0.0.1", port=2947)
## Esperar hasta obtener una fijación 2D
#while True:
#    packet = gpsd.get_current()
#    if packet.mode >= 2:
#        break
#    print("Esperando una fijación 2D...")
#    time.sleep(1)
#
## Imprimir la posición
#print("Latitude: ", packet.lat)
#print("Longitude: ", packet.lon)
#print("Altitude: ", packet.alt)
from gps3 import gps3

# Conexión al servicio gpsd
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()

gps_socket.connect(host="127.0.0.1", port=2947)
gps_socket.watch()

try:
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print('Latitud = {}, Longitud = {}, Altitud = {}'.format(
                data_stream.TPV['lat'], data_stream.TPV['lon'], data_stream.TPV['alt']))
            
except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    gps_socket.close()
