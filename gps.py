import gps

# GPS-Verbindung herstellen
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        # Daten von GPS-Modul empfangen
        report = session.next()

        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                latitude = report.lat
                longitude = report.lon
                print("Latitude: ", latitude)
                print("Longitude: ", longitude)

    except KeyboardInterrupt:
        # Skript bei Tastaturunterbrechung beenden
        break

    except StopIteration:
        # GPS-Stream beendet
        print("GPS-Stream beendet")

