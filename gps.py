import serial

# Serielle Schnittstelle konfigurieren
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# Endlosschleife zum Lesen der GPS-Daten
while True:
    # Zeile von der seriellen Schnittstelle lesen
    line = ser.readline().decode('utf-8').strip()

    # Nur die NMEA-Zeilen verarbeiten
    if line.startswith('$GNGGA'):
        data = line.split(',')

        # Positionsinformationen extrahieren
        latitude = data[2]
        longitude = data[4]
        altitude = data[9]

        # Ausgabe der GPS-Daten
        print('Latitude: {}'.format(latitude))
        print('Longitude: {}'.format(longitude))
        print('Altitude: {}'.format(altitude))

# Serielle Verbindung schließen
ser.close()
