from datetime import datetime
from math import (exp, atan)

import os.path
from constants import *
import utils




"""
Class for reading data from data files 
and extracting data values as a two-dimensional list.

Members:
    filename    string, filename to be read
    indices     int list, indices of columns whose data 
                should be extracted  
    time_max    int, maximum time from now to the past in seconds 
                from which data should be read
    unix_times  int list, list of unix times 
                that correspond to the read data
    data        list of float lists, 2D list that contains the read data
"""
class DataFileReader:
    
    """
    Constructor, sets the filename, indices, the maximum time, 
    and declares the unix_time list and the 2D data list.
    
    @param filename     string, name of file to be read from
    @param indices      int list, list of column indices
                        from which data should be extracted
    @time_max           int, maximum time from now to the past 
                        for which data should still be read
    """
    def __init__(self, filename, indices, time_max=None):
        self.filename = filename
        self.indices = indices
        self.time_max = time_max
        self.unix_times = []
        self.data = [[0.0]*len(indices)]



    """
    Checks if the data of a particular line are within the time range
    from now to the past from which data should still be read.
    
    @param line     string, line to be checked for
    
    @return         boolean, 'True' if time if line is within 
                    the given range, 'False' otherwise 
    """
    def is_within_time_range(self, line):
        words = line.split('\t')
        unix_time = utils.get_unix_time(words[IDX_DATE], words[IDX_TIME])
        if (unix_time > unix_time_now - time_max):
            return True
        return False


    
    """
    Reads the data from self.filename and fills self.data with the extracted fields.
    """
    def read_data(self):
        unix_time_now = datetime.now().timestamp()
        filepath = os.path.join(PATH_DATA, self.filename)
        
        lines_all = []
        lines = []
       
        with open(filepath, 'r') as file_data:
            lines_all = file_data.readlines()
        
        if self.time_max is None:
            count = 0
        else:
            count = utils.get_index_of_first_line_within_time_range(lines_all, unix_time_now, self.time_max)
        lines = lines_all[count:]
        
        self.data = [[0.0 for x in range(len(lines))] for y in range(len(self.indices))]

        for j, line in enumerate(lines):
            words = line.split('\t')
            unix_time = utils.get_unix_time(words[IDX_DATE], words[IDX_TIME])
            
            self.unix_times.append(unix_time)
            for i, index in enumerate(self.indices):
                self.data[i][j] = float(words[index])
            
        
        


 
