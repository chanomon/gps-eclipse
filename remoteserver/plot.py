import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime


directorio = input('Write the ubication path of your json files )')


#start_time_str = input("Ingrese el start time en el formato 'YYYY-MM-DDTHH:MM:SS': ")
#end_time_str = input("Ingrese el end time en el formato 'YYYY-MM-DDTHH:MM:SS': ")


#start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
#end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')
# Obtener la lista de archivos JSON en el directorio
jsonfiles = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.json')]
print(jsonfiles)
df = pd.DataFrame(columns=['Time', 'SNR'])
snr_values = []
time = []

# Iterar sobre los archivos JSON, cargar los datos y extraer 'Time' y 'SNR'
for jfile in jsonfiles:
    with open(jfile, 'r') as file:
        data = json.load(file)

# Obtener los valores de 'SNR' de todos los registros de satélites
        for record in data:
            #df['Time'] = pd.to_datetime(record['Time'])
            for satellite in record['Satellites']:
                time.append(datetime.strptime(record['Time'],'%Y-%m-%dT%H:%M:%S.%fZ'))
                snr_values.append(float(satellite['SNR']))
                
        
#print(snr_values)
    #df = df.append(datos[['Time', 'SNR']])
#print(datos['Time'])
#print(datos['Satellites'][['SNR']])

# Convertir la columna de fecha/hora a formato datetime
#df['Time'] = pd.to_datetime(df['Time'])

# Graficar la serie de tiempo para la columna 'SNR'
plt.figure(figsize=(10, 6))
plt.scatter(time, snr_values)
plt.xlabel('Tiempo')
plt.ylabel('SNR')
#plt.title()
plt.show()
