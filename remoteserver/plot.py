import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="Scropt to proccess json files and make SNR plots")
#parser.add_argument("directory", type=str, help="Ubication of json files")
parser.add_argument("directories", type=str, nargs='+', help="Ubications of json files")

args = parser.parse_args()

directories = args.directories
plotpath = input('write the path where you want to save your plot )')

#df = pd.DataFrame(columns=['Time', 'SNR'])
snr_values = []
time = []
for directorio in directories:
    #print(directorio)
    jsonfiles = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.json')]
    #print(jsonfiles)
    for jfile in jsonfiles:
        with open(directorio+'/'+jfile, 'r') as file:
            #print(directorio+'/'+jfile)
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

plt.savefig(plotpath)
plt.show()
#plt.title()
