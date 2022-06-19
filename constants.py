import os.path

from config import *
from config_mail import *




# derived paths
PATH_WEATHER = os.path.join(PATH_HOME, 'weather')
PATH_SENSORS = os.path.join(PATH_HOME, 'sensors')
PATH_DATA = os.path.join(PATH_WEATHER, 'data')
PATH_LOGS = os.path.join(PATH_WEATHER, 'logs')
PATH_IMAGES_MAIL = os.path.join(PATH_WEATHER, 'images')
PATH_IMAGES_WEB = os.path.join(PATH_HTML, 'images')
# filenames
FILE_CONTINUOUS = 'continuous_weather.txt'
FILE_T_MIN_AVG_MAX = 'T_min_avg_max.txt'
FILE_HTML = 'index.html'
FILE_LOG = 'weather.log'
# image formats
IMAGE_FORMAT_WEB = 'svg'
IMAGE_FORMAT_MAIL = 'pdf'
# file prefixed
PREFIX_24H = '24h'
PREFIX_48H = '48h'
PREFIX_7D = '7d'
PREFIX_31D = '31d'
PREFIX_365D = '365d'
PREFIX_31D_AVG = '31d_AVG'
PREFIX_365D_AVG = '365d_AVG'
# logging
LOG_SUCCESS_AVERAGE_PLOTS = 'Successfully created average plots.'
LOG_SUCCESS_RAW_DATA_PLOTS = 'Successfully created raw data plots.'
LOG_SUCCESS_E_MAILS = 'Successfully sent e-mails.'
# xlabels
XLABEL_DAY = 'Daily Hour'
XLABEL_WEEK = 'Weekday'
XLABEL_MONTH = ''
# time between two measurements in seconds
TIME_DATA = 15*60
# maximum time span between first and last
# times for 24 hours plots in seconds
TIME_DAY = 24*60*60
TIME_MINOR_TICKS_DAY = 15*60
TIME_MAJOR_TICKS_DAY = 60*60
TIME_MAJOR_TICK_LABELS_DAY = 2*60*60    
# maximum time span between first and last
# times for 48 hours plots in seconds
TIME_2DAYS = 2*TIME_DAY
TIME_MINOR_TICKS_2DAYS = 30*60
TIME_MAJOR_TICKS_2DAYS = 2*60*60
TIME_MAJOR_TICK_LABELS_2DAYS = 4*60*60    
# maximum time span between first and last
# times for 7 days plots in seconds
TIME_WEEK = 7*TIME_DAY
TIME_MINOR_TICKS_WEEK = 6*60*60
TIME_MAJOR_TICKS_WEEK = 12*60*60
TIME_MAJOR_TICK_LABELS_WEEK = 24*60*60    
# maximum time span between first and last
# times for 31 days plots in seconds
TIME_MONTH = 31*TIME_DAY
TIME_MINOR_TICKS_MONTH = TIME_DAY
TIME_MAJOR_TICKS_MONTH = 7*TIME_DAY
TIME_MAJOR_TICK_LABELS_MONTH = 7*TIME_DAY
# maximum time span between first and last
# times for 365 days plots in seconds
TIME_YEAR = 365*TIME_DAY
TIME_MINOR_TICKS_YEAR = TIME_WEEK
TIME_MAJOR_TICKS_YEAR = 4*TIME_WEEK
TIME_MAJOR_TICK_LABELS_YEAR = 4*TIME_WEEK
# parameter collection for plots for days, weeks, and years
PARAMETERS_DAY = [XLABEL_DAY,
                  TIME_DAY,
                  TIME_MINOR_TICKS_DAY,
                  TIME_MAJOR_TICKS_DAY,
                  TIME_MAJOR_TICK_LABELS_DAY]

PARAMETERS_2DAYS = [XLABEL_DAY,
                    TIME_2DAYS,
                    TIME_MINOR_TICKS_2DAYS,
                    TIME_MAJOR_TICKS_2DAYS,
                    TIME_MAJOR_TICK_LABELS_2DAYS]

PARAMETERS_WEEK = [XLABEL_WEEK,
                   TIME_WEEK,
                   TIME_MINOR_TICKS_WEEK,
                   TIME_MAJOR_TICKS_WEEK,
                   TIME_MAJOR_TICK_LABELS_WEEK]

PARAMETERS_MONTH = [XLABEL_MONTH,
                    TIME_MONTH,
                    TIME_MINOR_TICKS_MONTH,
                    TIME_MAJOR_TICKS_MONTH,
                    TIME_MAJOR_TICK_LABELS_MONTH]

PARAMETERS_YEAR = [XLABEL_MONTH,
                   TIME_YEAR,
                   TIME_MINOR_TICKS_YEAR,
                   TIME_MAJOR_TICKS_YEAR,
                   TIME_MAJOR_TICK_LABELS_YEAR]

# indices of fields to be plotted from the 2D array of all data
IDX_DATE = 0
IDX_TIME = 1
IDX_TEMPERATURE = 2
IDX_PRESSURE_RAW = 3
IDX_PRESSURE_SEA = 4
IDX_HUMIDITY_REL = 5
IDX_HUMIDITY_ABS = 6

NUMBER_OF_INDICES = 7

IDX_MIN = 2
IDX_AVG = 3
IDX_MAX = 4

NUMBER_OF_INDICES_AVG = 5

LABEL_TEMPERATURE = 'Temperature'
LABEL_PRESSURE_RAW = 'Raw Pressure'
LABEL_PRESSURE_SEA = 'Sea Level Pressure'
LABEL_HUMIDITY_REL = 'Relative Humidity'
LABEL_HUMIDITY_ABS = 'Absolute Humidity'

UNIT_TEMPERATURE = '°C'
UNIT_PRESSURE = 'hPA'
UNIT_HUMIDITY_REL = '%'
UNIT_HUMIDITY_ABS = 'g/m³'

PARAMETERS_TEMPERATURE = [LABEL_TEMPERATURE, 
                          UNIT_TEMPERATURE, 
                          COLOR_TEMPERATURE, 
                          LINESTYLE_TEMPERATURE]
PARAMETERS_PRESSURE_RAW = [LABEL_PRESSURE_RAW, 
                           UNIT_PRESSURE, 
                           COLOR_PRESSURE_RAW, 
                           LINESTYLE_PRESSURE_RAW]
PARAMETERS_PRESSURE_SEA = [LABEL_PRESSURE_SEA, 
                           UNIT_PRESSURE, 
                           COLOR_PRESSURE_SEA, 
                           LINESTYLE_PRESSURE_SEA]
PARAMETERS_HUMIDITY_REL = [LABEL_HUMIDITY_REL, 
                           UNIT_HUMIDITY_REL, 
                           COLOR_HUMIDITY_REL, 
                           LINESTYLE_HUMIDITY_REL]
PARAMETERS_HUMIDITY_ABS = [LABEL_HUMIDITY_ABS, 
                           UNIT_HUMIDITY_ABS, 
                           COLOR_HUMIDITY_ABS, 
                           LINESTYLE_HUMIDITY_ABS]

DICT_IDX_PARAMETERS = {
    IDX_TEMPERATURE : PARAMETERS_TEMPERATURE,
    IDX_PRESSURE_RAW : PARAMETERS_PRESSURE_RAW,
    IDX_PRESSURE_SEA : PARAMETERS_PRESSURE_SEA,
    IDX_HUMIDITY_REL : PARAMETERS_HUMIDITY_REL,
    IDX_HUMIDITY_ABS : PARAMETERS_HUMIDITY_ABS
}

DICT_IDX_LINESTYLES = {
    IDX_MIN : LINESTYLE_MIN,
    IDX_AVG : LINESTYLE_AVG,
    IDX_MAX : LINESTYLE_MAX
}
