import serial

# Serielle Schnittstelle konfigurieren
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
print(ser)

# Endlosschleife zum Lesen der GPS-Daten
while True:
    # Zeile von der seriellen Schnittstelle lesen
    line = ser.readline().decode('ascii').strip()
    print(line)

    # Nur die NMEA-Zeilen verarbeiten
    if line.startswith('$GNGGA'):
        data = line.split(',')
        print("data", data)
#         # Positionsinformationen extrahieren
#         latitude = data[2]
#         longitude = data[4]
#         altitude = data[9]
#
#         # Ausgabe der GPS-Daten
#         print('Latitude: {}'.format(latitude))
#         print('Longitude: {}'.format(longitude))
#         print('Altitude: {}'.format(altitude))
#     if line.startswith('$GNRMC'):
#         gps_data = line.split(',')
#         print("gps_data", gps_data)
#         # Breitengrad und Längengrad extrahieren
#         latitude = gps_data[3]
#         longitude = gps_data[5]
#
#         # Ausgabe der GPS-Daten
#         print('Latitude:', latitude)
#         print('Longitude:', longitude)
#
# # Serielle Verbindung schließen
# ser.close()
