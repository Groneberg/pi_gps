# import serial
#
# # Serielle Schnittstelle konfigurieren
# ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
# print(ser)
#
# # Endlosschleife zum Lesen der GPS-Daten
# while True:
#     # Zeile von der seriellen Schnittstelle lesen
#     line = ser.readline().decode('utf-8').strip()
#     print(line)
#
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
#
# # Serielle Verbindung schließen
# ser.close()

import serial
from time import sleep

# Funktion zur GPS-Informationsermittlung
def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = NMEA_buff[0]  # Zeit aus dem GPGGA-String extrahieren
    nmea_latitude = NMEA_buff[1]  # Breitengrad aus dem GPGGA-String extrahieren
    nmea_longitude = NMEA_buff[3]  # Längengrad aus dem GPGGA-String extrahieren

    print("NMEA Time: ", nmea_time, '\n')
    print("NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, '\n')

    lat = float(nmea_latitude)  # String in eine Gleitkommazahl für Berechnungen umwandeln
    longi = float(nmea_longitude)  # String in eine Gleitkommazahl für Berechnungen umwandeln

    lat_in_degrees = convert_to_degrees(lat)  # Breitengrad im Dezimalformat erhalten
    long_in_degrees = convert_to_degrees(longi)  # Längengrad im Dezimalformat erhalten


# Funktion zur Konvertierung der rohen NMEA-Zeichenkette in das Grad-Dezimalformat
def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    position = degrees + mm_mmmm
    position = "%.4f" % (position)
    return position


gpgga_info = "$GPGGA,"
ser = serial.Serial("/dev/ttyS0")  # Port mit Baudrate öffnen
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

try:
    while True:
        received_data = str(ser.readline())  # Empfangene NMEA-Zeichenkette lesen
        GPGGA_data_available = received_data.find(gpgga_info)  # Nach NMEA GPGGA-Zeichenkette suchen
        if GPGGA_data_available > 0:
            GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]  # Daten nach der Zeichenkette "$GPGGA," speichern
            NMEA_buff = GPGGA_buffer.split(',')  # Durch Kommas getrennte Daten im Puffer speichern
            GPS_Info()  # Zeit, Breitengrad, Längengrad abrufen

            print("lat in degrees:", lat_in_degrees, " long in degree: ", long_in_degrees, '\n')
            # Link erstellen, um den Standort auf Google Maps anzuzeigen
            map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees
            print("<<<<<<<<<<<press ctrl+c to plot location on google maps>>>>>>>>>>\n")
            print("------------------------------------------------------------\n")

except KeyboardInterrupt:
    # Aktuelle Positionsinformationen in Google Maps öffnen
    webbrowser.open(map_link)
