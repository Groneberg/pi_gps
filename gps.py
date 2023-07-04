import serial

# Serielle Schnittstelle konfigurieren
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
print(ser)

# Endlosschleife zum Lesen der GPS-Daten
while True:
    try:
        # Zeile von der seriellen Schnittstelle lesen
        # line = ser.readline().decode('utf-8').strip()
        line = ser.readline().decode('latin-1').strip()
        print(line)

        # Nur die NMEA-Zeilen verarbeiten
        if line.startswith('$GNGGA'):
            GNGGA_data = line.split(',')
            print("UTC-Zeit:", GNGGA_data[1])
            print("Breitengrad:", GNGGA_data[2])
            print("Breitengrad-Richtung:", GNGGA_data[3])
            print("Längengrad:", GNGGA_data[4])
            print("Längengrad-Richtung:", GNGGA_data[5])
            print("GPS-Qualitätsindikator:", GNGGA_data[6])
            print("Anzahl der verwendeten Satelliten:", GNGGA_data[7])
            print("HDOP:", GNGGA_data[8])
            print("Höhe über dem Meeresspiegel:", GNGGA_data[9])
            print("Höheneinheit:", GNGGA_data[10])
            print("Geoid-Höhe:", GNGGA_data[11])
            print("Geoid-Höhen-Einheit:", GNGGA_data[12])
            print("Zeit seit der letzten DGPS-Aktualisierung:", GNGGA_data[13])
            print("DGPS-Referenzstation-ID:", GNGGA_data[14])

    #         # Positionsinformationen extrahieren
    #         latitude = data[2]
    #         longitude = data[4]
    #         altitude = data[9]
    #
    #         # Ausgabe der GPS-Daten
    #         print('Latitude: {}'.format(latitude))
    #         print('Longitude: {}'.format(longitude))
    #         print('Altitude: {}'.format(altitude))
        if line.startswith('$GNRMC'):
            GNRMC_data = line.split(',')
            print("Status:", GNRMC_data[2])
            print("Geschwindigkeit über Grund:", GNRMC_data[7])
            print("Modus:", GNRMC_data[12])
    #         # Breitengrad und Längengrad extrahieren
    #         latitude = gps_data[3]
    #         longitude = gps_data[5]
    #
    #         # Ausgabe der GPS-Daten
    #         print('Latitude:', latitude)
    #         print('Longitude:', longitude)
    except Exception as e:
        print("Fehler:", str(e))  # Fehlermeldung ausgeben

# # Serielle Verbindung schließen
# ser.close()
