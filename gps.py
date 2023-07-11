import serial
from datetime import datetime


class GPS:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
    utc_time: datetime = 0
    latitude: float = 0
    latitude_direction: str = 0
    longitude: float = 0
    longitude_direction: str = 0
    gps_quality_indicator: int = 0
    number_of_satellites_used: int = 0
    hdop: float = 0
    altitude: float = 0
    altitude_unit: str = ""
    geo_id_altitude: float = 0
    geo_id_altitude_unit: str = ""
    time_since_last_dgps_update: str = ""
    dgps_reference_station_id: str = ""
    velocity: float = 0
    course: float = None
    magnetic_divergence: float = 0
    magnetic_divergence_direction: str = ""
    status: str = ""
    mode: str = ""

    def extract_data(self):
        line = self.ser.readline().decode('utf-8').strip()

        if line.startswith('$GNGGA'):
            gngga_data = line.split(',')
            print("utc-time", gngga_data[1])
            self.utc_time = datetime.strptime(gngga_data[1], "%H%M%S.%f")
            self.latitude = float(gngga_data[2])
            self.latitude_direction = gngga_data[3]
            self.longitude = float(gngga_data[4])
            self.longitude_direction = gngga_data[5]
            self.gps_quality_indicator = int(gngga_data[6])
            self.number_of_satellites_used = int(gngga_data[7])
            self.hdop = float(gngga_data[8])
            self.altitude = float(gngga_data[9])
            self.altitude_unit = gngga_data[10]
            self.geo_id_altitude = float(gngga_data[11])
            self.geo_id_altitude_unit = gngga_data[12]
            self.time_since_last_dgps_update = gngga_data[13]
            self.dgps_reference_station_id = gngga_data[14]

        if line.startswith('$GNRMC'):
            gnrmc_data = line.split(',')
            self.status = gnrmc_data[2]
            self.velocity = float(gnrmc_data[7])
            self.course = float(gnrmc_data[8])
            self.magnetic_divergence = float(gnrmc_data[10])
            self.magnetic_divergence_direction = gnrmc_data[11]
            print("mode", gnrmc_data[12])
            self.mode = gnrmc_data[12]

    def get_data(self):
        return {
            "utc_time": self.utc_time,
            "latitude": self.latitude,
            "latitude_direction": self.latitude_direction,
            "longitude": self.longitude,
            "longitude_direction": self.longitude_direction,
            "gps_quality_indicator": self.gps_quality_indicator,
            "number_of_satellites_used": self.number_of_satellites_used,
            "hdop": self.hdop,
            "altitude": self.altitude,
            "altitude_unit": self.altitude_unit,
            "geo_id_altitude": self.geo_id_altitude,
            "geo_id_altitude_unit": self.geo_id_altitude_unit,
            "time_since_last_dgps_update": self.time_since_last_dgps_update,
            "dgps_reference_station_id": self.dgps_reference_station_id,
            "velocity": self.velocity,
            "course": self.course,
            "magnetic_divergence": self.magnetic_divergence,
            "magnetic_divergence_direction": self.magnetic_divergence_direction,
            "status": self.status,
            "mode": self.mode
        }


# Endlosschleife zum Lesen der GPS-Daten
gps = GPS()
while True:
    try:
        gps.extract_data()
        data = gps.get_data()
        print(data)
    except Exception as e:
        print("Fehler:", str(e))  # Fehlermeldung ausgeben


