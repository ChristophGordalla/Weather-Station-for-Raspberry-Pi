#!/usr/bin/python3



import os
import sys
import logging
from datetime import datetime

from constants import *
import utils
from reader import DataFileReader
from writer import DataFileWriter
from plot import PlotCreation
from mail import MailSender

logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(PATH_LOGS, FILE_LOG), level=logging.INFO)




"""
Reads data from the last 24h and 15min from the continuous data file
and uses them to compute the daily minimum, maximum, and time average 
of a given field. Also the average date and time of the given times is computed.
Then these values are written to a data file.

@param index_column     column index of the quantity to determine min, max, and avg from
@param file_data        string, name of file to write min, max, average, and date date to
"""
def write_min_max_avg_line_values(index_column, file_data):
    reader = DataFileReader(FILE_CONTINUOUS, [index_column], TIME_DAY+TIME_DATA)
    reader.read_data()
    
    values = reader.data[0]
    
    minimum = str(min(values))
    maximum = str(max(values))
    average = '{0:0.1f}'.format(utils.get_time_avg(reader.unix_times, values))
    unix_time_avg = utils.get_time_avg(reader.unix_times, reader.unix_times)
    
    line_values = ['']*NUMBER_OF_INDICES_AVG
    
    line_values[IDX_DATE] = datetime.fromtimestamp(unix_time_avg).strftime('%Y-%m-%d')
    line_values[IDX_TIME] = datetime.fromtimestamp(unix_time_avg).strftime('%H:%M')
    line_values[IDX_MIN] = minimum
    line_values[IDX_AVG] = average
    line_values[IDX_MAX] = maximum
    
    with open(os.path.join(PATH_DATA, file_data), 'a') as f:
        f.write('\t'.join(line_values) + '\n')
    


"""
Reads data from a given file with average data and creates the corresponding plots.

@param file_data            string, name of the data file
"""
def create_avg_data_plots(file_data):
    reader = DataFileReader(file_data, [IDX_MIN, IDX_AVG, IDX_MAX], TIME_MONTH)
    reader.read_data()
    plot = PlotCreation(reader.unix_times, reader.data, PATH_IMAGES_WEB, PREFIX_31D_AVG, IMAGE_FORMAT_WEB, PARAMETERS_TEMPERATURE, PARAMETERS_MONTH)
    plot.create_plot()
    
    reader = DataFileReader(file_data, [IDX_MIN, IDX_AVG, IDX_MAX], TIME_YEAR)
    reader.read_data()
    plot = PlotCreation(reader.unix_times, reader.data, PATH_IMAGES_WEB, PREFIX_365D_AVG, IMAGE_FORMAT_WEB, PARAMETERS_TEMPERATURE, PARAMETERS_YEAR)
    plot.create_plot()

    

"""
Creates plots of raw data (so without evaluating the min, max, and average
of data).

@param file_data            string, name of the data file
@param time_max             int, maximum time in seconds to cover the image data
@param indices              int list, indices of the columns from the data files
                            from which plots shall be generated
@param parameters_time      string list, collection of plot parameters 
                            (such as title, color, etc.)
@param image_path           string, path to store the image to
@param image_prefix         string, image prefix (e.g., the date of the data)
@param image_format         string, format of the image (without dot)
"""
def create_raw_data_plots(file_data, time_max, indices, parameters_time, image_path, image_prefix, image_format):
    reader = DataFileReader(file_data, indices, time_max)
    reader.read_data()
    
    for i, index in enumerate(indices):
        plot = PlotCreation(reader.unix_times, [reader.data[i]], 
                            image_path, image_prefix, image_format, 
                            DICT_IDX_PARAMETERS[index], parameters_time)
        plot.create_plot()
   


"""
Is called by crontab at 00:05 every day.
* It evaluates min, max, and average for the temperature values the day before.
* It creates plots of the data aquired the day before.
* These plots are automatically sent by mail.
"""
def do_daily_mode():
    unix_time_yesterday = datetime.now().timestamp() - TIME_DAY
    date_yesterday = datetime.fromtimestamp(unix_time_yesterday).strftime('%Y-%m-%d')
    
    # operations related with average data
    write_min_max_avg_line_values(IDX_TEMPERATURE, FILE_T_MIN_AVG_MAX)
    create_avg_data_plots(FILE_T_MIN_AVG_MAX)
    logging.info(LOG_SUCCESS_AVERAGE_PLOTS)
    
    # operations related with raw data data
    indices = [IDX_TEMPERATURE, IDX_PRESSURE_SEA, IDX_HUMIDITY_REL] 
    create_raw_data_plots(date_yesterday+'_weather.txt', None, indices, PARAMETERS_DAY, PATH_IMAGES_MAIL, date_yesterday, IMAGE_FORMAT_MAIL)
    logging.info(LOG_SUCCESS_RAW_DATA_PLOTS)
    
    # operations related with sending data
    files_images = [os.path.join(PATH_IMAGES_MAIL, i) for i in os.listdir(PATH_IMAGES_MAIL) if os.path.isfile(os.path.join(PATH_IMAGES_MAIL, i)) and i.startswith(date_yesterday)]
    files_data = [os.path.join(PATH_DATA, i) for i in os.listdir(PATH_DATA) if os.path.isfile(os.path.join(PATH_DATA, i)) and i.startswith(date_yesterday)]
    files_all = files_images + files_data

    my_mail_sender = MailSender(files_all, MAIL_SENDER, MAIL_PASSWORD, MAIL_RECIPENTS, 'Weather from '+date_yesterday, '')
    my_mail_sender.send_gmail()
    logging.info(LOG_SUCCESS_E_MAILS)



"""
Is called by crontab every 15 minutes and performs a data aquisition 
and creates new 24 hours, 7 days, 31 days, and 365 days plots 
with the acquired data. 
"""
def do_continuous_mode():
    writer = DataFileWriter()
    writer.write_to_files()
    
    indices_24h = [IDX_TEMPERATURE, IDX_PRESSURE_SEA, IDX_HUMIDITY_REL]
    indices_7d = [IDX_TEMPERATURE, IDX_PRESSURE_SEA, IDX_HUMIDITY_REL]
    indices_31d = [IDX_PRESSURE_SEA]
    indices_365d = [IDX_PRESSURE_SEA]
    
    create_raw_data_plots(FILE_CONTINUOUS, TIME_DAY, indices_24h, PARAMETERS_DAY, PATH_IMAGES_WEB, PREFIX_24H, IMAGE_FORMAT_WEB)
    create_raw_data_plots(FILE_CONTINUOUS, TIME_WEEK, indices_7d, PARAMETERS_WEEK, PATH_IMAGES_WEB, PREFIX_7D, IMAGE_FORMAT_WEB)
    create_raw_data_plots(FILE_CONTINUOUS, TIME_MONTH, indices_31d, PARAMETERS_MONTH, PATH_IMAGES_WEB, PREFIX_31D, IMAGE_FORMAT_WEB)
    create_raw_data_plots(FILE_CONTINUOUS, TIME_YEAR, indices_365d, PARAMETERS_YEAR, PATH_IMAGES_WEB, PREFIX_365D, IMAGE_FORMAT_WEB)
    
    logging.info(LOG_SUCCESS_RAW_DATA_PLOTS)



"""
Run this script with one of the following parameters:

continuous  Continous data acquisition and plot update.
daily       Generation of the plots from last day's data.
            The corresponding plots are then sent by mail.
"""
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'continuous':
            do_continuous_mode()
        elif sys.argv[1] == 'daily':
            do_daily_mode()
    except:
        logging.exception('Exception stack trace:\n')

