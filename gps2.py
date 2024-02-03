from gps import gps, WATCH_ENABLE

# Conectarse al demonio gpsd
session = gps(mode=WATCH_ENABLE)

try:
    while True:
        report = session.next()
        if report['class'] == 'TPV':
            # Información de posición y tiempo
            time_ = getattr(report, 'time', 'N/A')
            lat = getattr(report, 'lat', 'N/A')
            lon = getattr(report, 'lon', 'N/A')
            alt = getattr(report, 'alt', 'N/A')
            print(f"Time: {time_}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")

        elif report['class'] == 'SKY':
            # Información de satélites
            satellites_info = getattr(report, 'satellites', [])
            print("Satellites:")
            for satellite in satellites_info:
                prn = getattr(satellite, 'PRN', 'N/A')
                elevation = getattr(satellite, 'el', 'N/A')
                azimuth = getattr(satellite, 'az', 'N/A')
                snr = getattr(satellite, 'ss', 'N/A')
                used = getattr(satellite, 'used', False)
                print(f"Sat PRN: {prn}, Elevation: {elevation}, Azimuth: {azimuth}, SNR: {snr}, Used: {used}")

except KeyboardInterrupt:
    print('\nCerrando la conexión con gpsd')
finally:
    session.close()
