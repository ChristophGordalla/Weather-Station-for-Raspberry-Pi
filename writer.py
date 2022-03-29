import os.path
from datetime import datetime
from math import (exp, atan)

from constants import *
from acqui import DataAcquisition
import utils




"""
Class for using the acquired data to updating data files
as well as html index file of your web server.

Members:
    sensor_data     DataAcquisition object containing the sensor data
    line_data       string, line with data written to the data files,
                    this line stores the following data separated by tabs:
                     * date, formatted as: %Y-%m-%d
                     * time, formatted as: %H:%M
                     * temperature (in degC, 1 decimal place)
                     * pressure (in Pa, no decimal places)
                     * humidity (in %, 1 decimal place)
    line_html       string, line with formated data for html file
    date_now        string, date of today, formatted as YY-mm-dd
    time_now        string, current time, formatted as HH:MM 
    unix_time_now   int, unix time when script is called
"""
class DataFileWriter:

    """
    Constructor, declares line_data, date_now, time_now, and unix_time_now.
    """
    def __init__(self):
        self.sensor_data = DataAcquisition()
        self.sensor_data.measure_data()

        self.line_data = ''
        self.line_html = ''
        self.date_now = ''
        self.time_now = ''
        self.unix_time_now = ''
        # extract date and time
        self.set_time_data()
        self.set_data_lines()



    """
    Sets date_now and time_now with the current date and time.
     * self.date_now, formatted as: %Y-%m-%d
     * self.time_now, formatted as: %H:%M
    """
    def set_time_data(self):
        now = datetime.now()
        self.unix_time_now = now.timestamp()
        self.time_now = now.strftime('%H:%M')
        self.date_now = now.strftime('%Y-%m-%d')

    
    
    """
    Reads values from the sensors BMP 180 and AM2321
    and sets self.line_data and self.line_html.
    """
    def set_data_lines(self):
        get_abs_hum = lambda T, rh: 6.112*exp(17.67*T/(T+243.5))*rh*2.1674/(273.15+T)

        temperature = '{0:0.1f}'.format(self.sensor_data.temperature)
        pressure_raw = '{0:0.2f}'.format(self.sensor_data.pressure_raw)
        pressure_sea_level = '{0:0.2f}'.format(self.sensor_data.pressure_sea_level)
        humidity_rel = '{0:0.1f}'.format(self.sensor_data.rel_humidity)
        humidity_abs = '{0:0.2f}'.format(get_abs_hum(self.sensor_data.temperature, self.sensor_data.rel_humidity))

        line_values = ['']*NUMBER_OF_INDICES
        line_values[IDX_DATE] = self.date_now
        line_values[IDX_TIME] = self.time_now
        line_values[IDX_TEMPERATURE] = temperature
        line_values[IDX_PRESSURE_RAW] = pressure_raw
        line_values[IDX_PRESSURE_SEA] = pressure_sea_level
        line_values[IDX_HUMIDITY_REL] = humidity_rel
        line_values[IDX_HUMIDITY_ABS] = humidity_abs

        self.line_data = '\t'.join(line_values) + '\n'
        self.line_html = '<table><tr><td>Last Update: </td><td>' + self.date_now + ', ' + self.time_now + '</td></tr>' \
                       + '<tr><td>Temperature: </td><td>' + temperature + ' &#8451;</td><tr>' \
                       + '<tr><td>Raw pressure: </td><td>' + pressure_raw + ' hPa</td></tr>' \
                       + '<tr><td>Sea level pressure: </td><td>' + pressure_sea_level + ' hPa</td></tr>' \
                       + '<tr><td>Relative Humidity: </td><td>' + humidity_rel + ' %</td></tr>' \
                       + '<tr><td>Absolute Humidity: </td><td>' + humidity_abs + ' g/m&sup3;</td></tr>' \
                       + '<tr><td>Altitude: </td><td>' + str(ALTITUDE) + ' m</td></tr></table>\n' 



    """
    Writes data a line to the daily file.
    """
    def write_data_daily(self):
        filepath = os.path.join(PATH_DATA, self.date_now+'_weather.txt')

        with open(filepath, 'a') as file_data:
            file_data.write(self.line_data)

        
        
    """
    Writes the new data line to the continuous data file. 
    After adding this new line of data, it checks if there 
    are lines that are older than a given maximum time compared
    to the time of the newly added line. If so, these line are removed.
    
    @param filename     string, name of the file to be edited 
                        (24h, 7d, or 31d data file)
    @param time_max     int, maximum time (in seconds) between 
                        the newly added data line and the oldest
                        data line still remaining in the file
    """
    def write_data_continuous(self, filename, time_max):
        filepath = os.path.join(PATH_DATA, filename)
        
        with open(filepath, 'r') as file_temp:
            lines = file_temp.readlines()
        
        count = utils.get_index_of_first_line_within_time_range(lines, self.unix_time_now, time_max)
        
        with open(filepath, 'w') as file_data:
            file_data.writelines(lines[count:])
            file_data.write(self.line_data)



    """
    Writes the html index file and updates 
    the 'Last Update: ' line of that file 
    with the current date, time, and data.
    """
    def write_html(self):
        filepath = os.path.join(PATH_HTML, FILE_HTML)
        
        with open(filepath, 'r') as file_temp:
            lines_html = file_temp.readlines()
        
        # Find line in html file containing the 'Last Update:' expression
        for i in range(len(lines_html)):
            if 'Last Update' in lines_html[i]:
                break
        
        lines_html[i] = self.line_html
        
        with open(filepath, 'w') as file_index:
            file_index.writelines(lines_html)



    """
    Writes a new data line to the daily file, 
    the 365 days data file, and the html file. 
    """
    def write_to_files(self):
        self.write_data_daily()
        self.write_data_continuous(FILE_CONTINUOUS, TIME_YEAR)
        self.write_html()
