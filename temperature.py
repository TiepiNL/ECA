'''
Functions to analyze the data provided by the ECA (European Climate Assessment),
available in big data files.
'''

from datetime import datetime
import pathlib


def read_textfile(filename):
    ''' (str) -> list

    Open text file 'filename' and return the content as a list of lines.
    '''
    file_path = pathlib.Path(filename)
    with file_path.open(mode='r', encoding='utf-8') as fopen:
        lines = fopen.readlines()

    return lines


def read_data(filename):
    ''' (str) -> tuple of list of str, list of float

    Convert an EUROPEAN CLIMATE ASSESSMENT & DATASET (ECA&D) text file
    into a list of dates and a list of temperatures.
    '''
    # Read the content of the text file with a helper function.
    lines = read_textfile(filename)

    list_of_dates = []
    list_of_temperatures = []
    # The text file starts with a multiline file header. We loop through the lines
    # until we find the data headers, meaning the data will start at the next line.
    data_line = False
    for line in lines:
        # Remove the trailing linebreak
        line = line.rstrip('\n')
        if data_line is False:
            if line.strip().startswith('STAID'):
                # Data header detected.
                data_line = True
        else:
            # Extract the date and the temperature from the data.
            # chars 15-22: Date (YYYYMMDD)
            # chars 24-28: Maximum temperature (in 0.1C)
            list_of_dates.append(line[14:22])
            # Convert the temperatures into C (floats) while processing.
            list_of_temperatures.append(int(line[23:28].strip()) / 10)

    return (list_of_dates, list_of_temperatures)


def get_highest_temp(list_of_dates, list_of_temperatures):
    ''' (list of str, list of int) -> tuple of str, int

    >>> max_dates = ['19010107', '19010108', '19010109']
    >>> max_temps = [-6.6, -0.6, 4.2]
    >>> get_highest_temp(max_dates, max_temps)
    ('19010109', 4.2)
    '''
    highest_temp = list_of_temperatures[0]
    highest_temp_date = list_of_dates[0]

    for i in range(0, len(list_of_temperatures)):
        if list_of_temperatures[i] > highest_temp:
            highest_temp = list_of_temperatures[i]
            highest_temp_date = list_of_dates[i]

    return (highest_temp_date, highest_temp)



def get_lowest_temp(list_of_dates, list_of_temperatures):
    ''' (list, list) -> tuple of str, int

    >>> min_dates = ['19010118', '19010119', '19010120']
    >>> min_temps = [-4.5, -0.4, 4.3]
    >>> get_lowest_temp(min_dates, min_temps)
    ('19010118', -4.5)
    '''
    lowest_temp = list_of_temperatures[0]
    lowest_temp_date = list_of_dates[0]

    for i in range(0, len(list_of_temperatures)):
        if list_of_temperatures[i] < lowest_temp:
            lowest_temp = list_of_temperatures[i]
            lowest_temp_date = list_of_dates[i]

    return (lowest_temp_date, lowest_temp)


def get_friendly_date(date):
    ''' (str) --> str

    Convert 'date' in a friendly format and return it.

    Precondition: the input date has a format of 'yyyymmdd'

    >>> get_friendly_date('19670503')
    '3 May 1967'
    '''
    date_obj = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    friendly_date = "{} {} {}".format(date_obj.day, date_obj.strftime('%B'), date_obj.year)

    return friendly_date


def get_longest_freezing(max_dates, max_temps):
    ''' (list of str, list of float) -> tuple of int, str

    >>> max_dates = ['19010107', '19010108', '19010109']
    >>> max_temps = [-6.6, -0.6, 4.2]
    >>> get_longest_freezing(max_dates, max_temps)
    (2, '19010108')
    '''
    uninterrupted_period = 0
    longest_uninterrupted_period = 0
    last_day = ''
    was_freezing = False
    for i in range(0, len(max_dates)):
        if max_temps[i] < 0:
            # If it was already freezing the previous day, add the current day
            # to the period count. Otherwise start at 1.
            if was_freezing:
                uninterrupted_period += 1
            else:
                was_freezing = True
                uninterrupted_period = 1
        elif was_freezing:
            # Only update return values if there's a new record.
            if uninterrupted_period > longest_uninterrupted_period:
                longest_uninterrupted_period = uninterrupted_period
                # The previous day was the last day of the freezing period.
                last_day = max_dates[i-1]
            # Reset the freezing period.
            was_freezing = False
    return (longest_uninterrupted_period, last_day)


# Assignment 0: reading the data
max_dates, max_temps = read_data('DeBiltTempMaxOLD.txt')
min_dates, min_temps = read_data('DeBiltTempMinOLD.txt')

# Assignment 1: extreme temperatures
highest_temp_date, highest_temp = get_highest_temp(max_dates, max_temps)
highest_temp_friendly_date = get_friendly_date(highest_temp_date)

lowest_temp_date, lowest_temp = get_lowest_temp(min_dates, min_temps)
lowest_temp_friendly_date = get_friendly_date(lowest_temp_date)

print("The highest temperature was {} degrees Celsius and was measured on {}.".format(
    highest_temp, highest_temp_friendly_date))
print("The lowest temperature was {} degrees Celsius and was measured on {}.".format(
    lowest_temp, lowest_temp_friendly_date))

# Assignment 2: cold colder coldest
uninterrupted_period, last_day = get_longest_freezing(max_dates, max_temps)
friendly_last_day = get_friendly_date(last_day)

print("The longest freezing period lasted {} days, end ended after {}.".format(
    uninterrupted_period, friendly_last_day))

# Assignment 3: summer days and tropical days




# Run docstring tests.
if __name__ == '__main__':
    import doctest
    doctest.testmod()
