from datetime import datetime

from constants import *



"""
Utility methods that are not directly connect to class members.
"""




"""
Returns the unix time for a given date and time of the day.     .
 
@param date     string, date, formatted as YYYY-MM-DD
@param time     string, time of the day, formatted as hh:mm 

@return         datetime object for the given date and time string
"""
def get_unix_time(date, time):
    (year, month, day) = date.split('-')
    (hour, minute) = time.split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp()



"""
Returns the index of the first line that is still within the given time range.

@param time_max         
@param unix_time_now    

@return                 int, index of line 
                        that is still within the given time range
"""
def get_index_of_first_line_within_time_range(lines, unix_time_now, time_max):
    count = 0
    words = lines[count].split('\t')
    
    unix_time_first = get_unix_time(words[0], words[1])
        
    while unix_time_first <= unix_time_now - time_max:
        count += 1
        words = lines[count].split('\t')
        unix_time_first = get_unix_time(words[0], words[1])

    return count



"""
Computes the time average for a given list of values.

@param times    int list, list of times in seconds for the value list
@param values   float list, list of values to be averaged

@return         float, time average of the given list
"""
def get_time_avg(times, values):
    N = len(times) 
    if N != len(values):
        print('ERROR, length of times and values differ.')
        return 
    
    avg = 0.

    for i in range(1, N):
        dt = times[i] - times[i-1]
        val_avg = 0.5*(values[i-1]+values[i])
        avg += dt*val_avg

    return avg/(times[N-1]-times[0])
