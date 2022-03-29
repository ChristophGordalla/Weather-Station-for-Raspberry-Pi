from subprocess import check_output 

#Import library for BMP085 barometric pressure/temperature/altitude Sensor.
#These libraries must be installed manually. 
#Adjust those imports if you use different sensors.
import Adafruit_BMP.BMP085 as BMP085

from constants import *



"""
Class to aquire the sensor data. Modify this files to your needs
to make it compliant with the sensors that you are using.

Members:
    temperature         float, temperature value (in degC)
    pressure_raw        float, raw pressure value 
                        that is measured by the sensor (in hPa)
    pressure_sea_level  float, corrected sea-level pressure value (in hPa)
    rel_humidity        float, relative humidity value (in %)
"""
class DataAcquisition:
    
    """
    Constructor, initiates all class members with 0.
    """
    def __init__(self):
        self.temperature = 0.
        self.pressure_raw = 0.
        self.pressure_sea_level = 0.
        self.rel_humidity = 0.


    """
    In this method, the actual data measurement takes place. 
    Modify this method if you use other sensors.

    Measures temperature (in degC), raw pressure (in hPa), 
    sea level pressure (in hPa), and relative humidity (in %).
    
    Used sensors: BMP085 for temperature and pressure values,
                  AM2321 for relative humidities
    """
    def measure_data(self):
        # BMP085 data
        bmp085 = BMP085.BMP085()
        self.temperature = bmp085.read_temperature()
        #p_bmp085 = bmp085.read_pressure()/100 #in hPa
        self.pressure_raw = bmp085.read_raw_pressure()/100 #in hPa
        self.pressure_sea_level = bmp085.read_sealevel_pressure(ALTITUDE)/100 #in hPa
        
        # AM2321 data
        output_am2321 = check_output([os.path.join(PATH_SENSORS, './am2321/am2321')]).decode('utf-8')[:-1]
        values_am2321 = output_am2321.split(" ")
        #T_am2321 = float(values_am2321[0])    # unused
        self.rel_humidity = float(values_am2321[1])
    
    
    

