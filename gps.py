import serial

# Serielle Verbindung herstellen
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

while True:
    # Daten von der seriellen Schnittstelle lesen
    line = ser.readline().decode('utf-8').rstrip()

    # Überprüfen, ob die Zeile GPS-Daten enthält
    if line.startswith('$GNRMC') or line.startswith('$GPRMC'):
        data = line.split(',')
        if data[2] == 'V':
            print("Keine gültigen GPS-Daten verfügbar")
        else:
            latitude = float(data[3][:2]) + float(data[3][2:]) / 60.0
            longitude = float(data[5][:3]) + float(data[5][3:]) / 60.0
            print("Latitude: ", latitude)
            print("Longitude: ", longitude)

# Serielle Verbindung schließen
ser.close()
