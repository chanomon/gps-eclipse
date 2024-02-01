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
            #print('Latitud = {}, Longitud = {}, Altitud = {}'.format(
            #    data_stream.TPV['lat'], data_stream.TPV['lon'], data_stream.TPV['alt']))
            # Cheking if 2D fix or 3D fix
            if data_stream.TPV['mode'] >= 2:
                print('Latitud: {}'.format(data_stream.TPV['lat']))
                print('Longitud: {}'.format(data_stream.TPV['lon']))
                print('Altitud: {}'.format(data_stream.TPV['alt']))
                print('Velocidad: {} m/s'.format(data_stream.TPV['speed']))
                print('Rumbo: {} grados'.format(data_stream.TPV['track']))
                print('Fecha: {}'.format(data_stream.TPV['time']))
                print('Número de satélites visibles: {}'.format(data_stream.TPV['satellites_visible']))
                print('Número de satélites utilizados: {}'.format(data_stream.TPV['satellites_used']))
                print('Precisión horizontal: {} m'.format(data_stream.TPV['eph']))
                print('Precisión vertical: {} m'.format(data_stream.TPV['epv']))
                print('Modo de solución de posición: {}'.format(data_stream.TPV['mode']))
                
            else:
                print('Esperando una fijación 2D o 3D...')

            
except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    gps_socket.close()
