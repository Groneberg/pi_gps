import serial

# Serielle Schnittstelle konfigurieren
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
print(ser)

# Endlosschleife zum Lesen der GPS-Daten
while True:
    # Zeile von der seriellen Schnittstelle lesen
    line = ser.readline().decode('utf-8').strip()
    # print(line)

    # Nur die NMEA-Zeilen verarbeiten
    if line.startswith('$GNGGA'):
        data = line.split(',')
        print("UTC-Zeit", data[1])
        print("Breitengrad", data[2])
        print("Breitengrad-Richtung", data[3])
        print("Längengrad", data[4])
        print("Längengrad-Richtung", data[5])
        print("GPS-Qualitätsindikator", data[6])
        print("Anzahl der verwendeten Satelliten", data[7])
        print("HDOP", data[8])
        print("Höhe über dem Meeresspiegel", data[9])
        print("Höheneinheit", data[10])
        print("Geoid-Höhe", data[11])
        print("Geoid-Höhen-Einheit", data[12])
        print("Zeit seit der letzten DGPS-Aktualisierung", data[13])
        print("DGPS-Referenzstation-ID", data[14])

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
