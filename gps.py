import serial

# Serielle Schnittstelle konfigurieren
ser1 = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
ser2 = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
ser3 = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
print("ser1", ser1)
print("----")
print("ser2", ser2)
print("----")
print("ser3", ser3)
print("----")


# Endlosschleife zum Lesen der GPS-Daten
while True:
    # Zeile von der seriellen Schnittstelle lesen
    line1 = ser1.readline().decode('utf-8').strip()
    print(line1)
    print("----1")
    line2 = ser2.readline().decode('utf-8').strip()
    print(line2)
    print("----2")
    line3 = ser3.readline().decode('utf-8').strip()
    print(line3)
    print("----3")

#     # Nur die NMEA-Zeilen verarbeiten
#     if line.startswith('$GNGGA'):
#         data = line.split(',')
#
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
#
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
