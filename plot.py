import os.path
import matplotlib
# use matplotlib without GUI
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from math import (exp, atan)
from datetime import datetime

from constants import *
from reader import DataFileReader
import utils




"""
Class to create the plots. This includes the
continuous 24h, 7d, and 31d plots, as well as the
daily plots in the end of every day.

Members:
    unix_times              int list, list of unix times in seconds 
                            for which the data will be plotted
    data                    2D float list, data to be plotted
    path_file               string, path and filename of the image to be generated
    label                   string, y-axis label
    color                   string, graph color
    linestyle               string, graph linestyle
    xlabel                  string, x-axis label 
    time_max                int, maximum time span for data to be plotted (in seconds),
                            e.g. 86400 for daily plots
    time_minor_ticks        int, time between two minor ticks in seconds 
    time_major_ticks        int, time between two major ticks in seconds
    time_major_tick_labels  int, time between two labeled major ticks in seconds
    indices                 int list, list of the indices for the fields from self.data to be plotted
    ticks                   float list, list of unix time tick values
    tick_labels             string list, list of tick labels
    OFFSET_TIME             int, total time offset in seconds (more explanation in ceil_to_next_multiple method

"""
class PlotCreation:
    
    """
    Constructor. Sets the class members and reads the data from the specified file. 

    @param unix_times               list, unix time values for the time to be set at the x-axis
    @param data                     2D list, data to be plotted; 
                                    for the regular plots, data has only one field/list as entry;
                                    for the min-avg-max plots, it has three fields/lists as entries
    @param path_image               string, path to the folder to store the created images
    @param prefix                   string, prefix of image file name (e.g., '24h_', '31d_', '31d_AVG_', etc.)
    @param image_format             string, format of the image without dot (e.g., 'svg', 'pdf', etc.)
    @param parameters_field         string list, parameters for plotting (e.g. label, unit, color, linestyle)
    @param parameters_time_period   list, parameters that are dependent on the time period of the plot (day, week, month),
                                    i.e.: label for x-axis, maximum time, major and minor ticks for time axis, 
                                    labels for major ticks
    """
    def __init__(self, unix_times, data, path_image, prefix, image_format, parameters_field, parameters_time_period):
        filename = '_'.join(parameters_field[0].split(' '))
        
        self.unix_times = unix_times
        self.data = data
        self.path_file = os.path.join(path_image, prefix+'_'+filename+'.'+image_format)
        self.label = parameters_field[0] + ' [' + parameters_field[1] + ']'
        self.color = parameters_field[2]
        self.linestyle = parameters_field[3]
        self.xlabel = parameters_time_period[0]
        self.time_max = parameters_time_period[1]
        self.time_minor_ticks = parameters_time_period[2]
        self.time_major_ticks =  parameters_time_period[3]
        self.time_major_tick_labels =  parameters_time_period[4]
        self.ticks = []
        self.tick_labels = []

        self.OFFSET_TIME = self.get_time_offset()

        (self.ticks, self.tick_labels) = self.unix_times_to_ticks(self.unix_times)
    

    
    """
    Get the total time offset needed for the modulo operation
    of the 'ceil_to_next_multiple function' (have a look there 
    for further explanation).

    @return     int, total time offset in seconds
    """
    def get_time_offset(self):
        OFFSET_THU_TO_MON = 4*TIME_DAY
        # use round functions since both function calls of the difference
        # are not called at exactly the same time
        OFFSET_TO_UTC = round(datetime.utcnow().timestamp()-datetime.now().timestamp())
        return OFFSET_THU_TO_MON + OFFSET_TO_UTC

    

    """
    Ceils a given value to the next full multiple of another number, e.g.:
    next_multiple_value(5.7, 3) -> 6 (=3*2).
    
    @param value    float, value to ceil from
    @param number   float, ceil to a multiple of this number 

    @return         float, ceiled value
    """
    def ceil_to_next_multiple(self, value, number):
        # The beginning of Unix time is 1970-01-01, 00:00 o'clock UTC.
        # This day was a Thursday. For the correct tick at the beginning 
        # of the calendar week, one has to offset the following modulo function
        # by the time to the next Monday (1970-01-05) and correct for the 
        # time difference to UTC (due to time zone as well as daylight saving time).
        modulo = (value - self.OFFSET_TIME) % number
        factor = 0 if modulo == 0 else 1 
        return (value - modulo) + factor*number 

    

    """
    Gets the tick label for a given unix time at the x-axis. 

    For plots over daily time spans: the number of the hour
    For plots over weekly time spans: the abbreviation of the week day (e.g. Wed)
    For plots over monthly/yearly time spans: CW + the calendar week + newline
                                     + the date (e.g. Oct 28)
    
    @param unix_time_tick_label     unix time at which a tick label should be extracted

    @return                         string, tick label
    """
    def get_tick_label(self, unix_time_tick_label):
        datetime_unix_time = datetime.fromtimestamp(unix_time_tick_label)
        if self.time_max < TIME_WEEK:
            hour = datetime_unix_time.strftime('%H')
            tick_label = hour[1] if hour[0] == '0' else hour
        elif self.time_max < TIME_MONTH:
            tick_label = datetime_unix_time.strftime('%a')
        else:
            #tick_label = datetime_unix_time.strftime('%d')
            tick_label = 'CW ' \
                       + str(datetime_unix_time.isocalendar()[1]) \
                       + '\n' + str(datetime_unix_time.strftime('%b %d'))
        return tick_label



    """
    Takes the list of taken unix_times and evaluates
    the position and label of the x-axis ticks.

    @param unix_times       string list, list of unix time values

    @return ticks           float list, list of unix time tick values
    @return tick_labels     string list, list of tick labels
    """
    def unix_times_to_ticks(self, unix_times):
        ticks = []
        tick_labels = []
        
        number_values = len(unix_times)
        
        unix_time_min = unix_times[0]
        unix_time_max = unix_times[number_values-1]
        unix_time_tick = self.ceil_to_next_multiple(unix_time_min, self.time_major_ticks)
        unix_time_tick_label = self.ceil_to_next_multiple(unix_time_min, self.time_major_tick_labels)

        while unix_time_tick < unix_time_max:
            ticks.append(unix_time_tick)
            if unix_time_tick == unix_time_tick_label:
                tick_label = self.get_tick_label(unix_time_tick_label)
                tick_labels.append(tick_label)
                unix_time_tick_label += self.time_major_tick_labels
            else:
                tick_labels.append('')
            unix_time_tick += self.time_major_ticks
            
        return ticks, tick_labels
     


    """
    Creates the actual plots according from the fields in self.data 
    which match the indices self.indices.
    """
    def create_plot(self):    
        fig, ax = plt.subplots()
            
        ax.set_xticks(self.ticks)
        ax.set_xticklabels(self.tick_labels) #, rotation='vertical')
        ax.xaxis.set_minor_locator(AutoMinorLocator(self.time_major_ticks//self.time_minor_ticks))
        ax.tick_params(which='minor', length=3)
        ax.tick_params(which='major', length=6)
        

        for field in self.data:
            plt.plot(self.unix_times, field, color=self.color, linestyle=self.linestyle)
        plt.margins(x=0.0)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.label)
        plt.grid(color='#dddddd')
        plt.savefig(self.path_file)
        plt.clf()
        plt.cla()
        plt.close()
