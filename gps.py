import gpsd

# Connect to the local gpsd
gpsd.connect()

# Get gps position
packet = gpsd.get_current()

# Check if there is a 2D fix
if packet.mode < 2:
    print("No 2D fix available yet. Waiting for a fix...")
else:
    # Print the position if there is a fix
    print("Latitude: ", packet.lat)
    print("Longitude: ", packet.lon)
    print("Altitude: ", packet.alt)

# See the inline docs for GpsResponse for other available data
