import math
import serial
from smbus2 import SMBus
from datetime import datetime


class GPS:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

    compass_address = 0x1E

    compass_x_register = 0x03
    compass_y_register = 0x05
    compass_z_register = 0x07

    bus = SMBus(1)
    gauss = 1.3
    __scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35],
    }

    (degrees, minutes) = (0, 0)
    __declDegrees = degrees
    __declMinutes = minutes
    __declination = (degrees + minutes / 60) * math.pi / 180
    (reg, __scale) = __scales[gauss]

    bus.write_byte_data(compass_address, 0x00, 0x70)  # 8 Average, 15 Hz, normal measurement
    bus.write_byte_data(compass_address, 0x01, reg << 5)  # Scale
    bus.write_byte_data(compass_address, 0x02, 0x00) # Continuous measurement

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
    # compas: float = None
    # compas_direction: str = None
    # deviation: float = None
    # deviation_direction: str = None
    compass_x = None
    compass_y = None
    compass_z = None


    def extract_data(self):
        line = self.ser.readline().decode('utf-8').strip()

        # Lese die Kompasswerte aus den Registern
        self.compass_x = self.bus.read_byte_data(self.compass_address, self.compass_x_register)
        self.compass_y = self.bus.read_byte_data(self.compass_address, self.compass_y_register)
        self.compass_z = self.bus.read_byte_data(self.compass_address, self.compass_z_register)




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


        # if line.startswith('$HCHDG'):
        #     hchdg_data = line.split(',')
        #     self.compas = float(hchdg_data[1])
        #     self.compas_direction = hchdg_data[2]
        #     self.deviation = float(hchdg_data[3])
        #     self.deviation_direction = hchdg_data[4]


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
            # "compas": self.compas,
            # "compas direction":self.compas_direction,
            # "deviation":self.deviation,
            # "deviation direction":self.deviation_direction,
            "compass_x":self.compass_x,
            "compass_y":self.compass_y,
            "compass_z":self.compass_z

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
        # data_str += f"Compas: {self.compas}\n"
        # data_str += f"Compas direction: {self.compas_direction}\n"
        # data_str += f"Deviation: {self.deviation}\n"
        # data_str += f"Deviation direction: {self.deviation_direction}\n"
        data_str += f"compass_x: {self.compass_x}\n"
        data_str += f"compass_y: {self.compass_y}\n"
        data_str += f"compass_z: {self.compass_z}\n"
        return data_str


# Endlosschleife zum Lesen der GPS-Daten
gps = GPS()
while True:
    try:
        gps.extract_data()
        data = gps.get_data()
        print(data)
    except Exception as e:
        print("Fehler:", str(e))  # Fehlermeldung ausgeben


