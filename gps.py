import serial
from smbus2 import SMBus
from datetime import datetime


class GPS:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
    bus = SMBus(1)
    utc_time: datetime = None
    latitude: float = None
    latitude_direction: str = None
    longitude: float = None
    longitude_direction: str = None
    gps_quality_indicator: int = None
    number_of_satellites_used: int = None
    hdop: float = None
    altitude: float = None
    altitude_unit: str = None
    geo_id_altitude: float = None
    geo_id_altitude_unit: str = None
    time_since_last_dgps_update: str = None
    dgps_reference_station_id: str = None
    velocity: float = None
    heading: float = None
    magnetic_divergence: float = None
    magnetic_divergence_direction: str = None
    status: str = None
    mode: str = None
    compas: float = None
    compas_direction: str = None
    deviation: float = None
    deviation_direction: str = None


    def extract_data(self):
        line = self.ser.readline().decode('utf-8').strip()
        b = self.bus.read_byte_data(10, 14)
        print("b", b)

        if line.startswith('$GNGGA'):
            gngga_data = line.split(',')
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
            self.heading = float(gnrmc_data[8])
            self.magnetic_divergence = float(gnrmc_data[10])
            self.magnetic_divergence_direction = gnrmc_data[11]
            self.mode = gnrmc_data[12]



        if line.startswith('$HCHDG'):
            hchdg_data = line.split(',')
            self.compas = float(hchdg_data[1])
            self.compas_direction = hchdg_data[2]
            self.deviation = float(hchdg_data[3])
            self.deviation_direction = hchdg_data[4]
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
            "heading": self.heading,
            "magnetic_divergence": self.magnetic_divergence,
            "magnetic_divergence_direction": self.magnetic_divergence_direction,
            "status": self.status,
            "mode": self.mode,
            "compas": self.compas,
            "compas direction":self.compas_direction,
            "deviation":self.deviation,
            "deviation direction":self.deviation_direction
        }

    def __str__(self):
        data_str = f"UTC Time: {self.utc_time}\n"
        data_str += f"Latitude: {self.latitude} {self.latitude_direction}\n"
        data_str += f"Longitude: {self.longitude} {self.longitude_direction}\n"
        data_str += f"GPS Quality Indicator: {self.gps_quality_indicator}\n"
        data_str += f"Number of Satellites Used: {self.number_of_satellites_used}\n"
        data_str += f"HDOP: {self.hdop}\n"
        data_str += f"Altitude: {self.altitude} {self.altitude_unit}\n"
        data_str += f"Geoid Altitude: {self.geo_id_altitude} {self.geo_id_altitude_unit}\n"
        data_str += f"Time Since Last DGPS Update: {self.time_since_last_dgps_update}\n"
        data_str += f"DGPS Reference Station ID: {self.dgps_reference_station_id}\n"
        data_str += f"Velocity: {self.velocity}\n"
        data_str += f"Heading: {self.heading}\n"
        data_str += f"Magnetic Divergence: {self.magnetic_divergence} {self.magnetic_divergence_direction}\n"
        data_str += f"Status: {self.status}\n"
        data_str += f"Mode: {self.mode}\n"
        data_str += f"Compas: {self.compas}\n"
        data_str += f"Compas direction: {self.compas_direction}\n"
        data_str += f"Deviation: {self.deviation}\n"
        data_str += f"Deviation direction: {self.deviation_direction}\n"
        return data_str


# Endlosschleife zum Lesen der GPS-Daten
gps = GPS()
while True:
    try:
        gps.extract_data()
        data = gps.get_data()
        gps.__str__()
    except Exception as e:
        print("Fehler:", str(e))  # Fehlermeldung ausgeben


