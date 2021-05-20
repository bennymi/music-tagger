from os import listdir
from os.path import isfile, join
import time

from lyrify.utils.constants import MONTHS
from lyrify.utils.errors import SongOrderError, SongOrderRangeError

def convert_date(date):
    """
    Converts date MM dd, yyyy to yyyymmdd format.
    Eg. 'June 12, 2013' -> '20130612'
    """
    new_date = ''
    date_parts = date.split(' ')
    new_date += date_parts[2] # year
    new_date += MONTHS[date_parts[0].lower()] # month
    new_date += date_parts[1].split(',')[0] # day
    return new_date

def parse_order(order):
    new_order = []
    for number in order:
        if number.isnumeric():
            new_order.append(int(number))
        elif '-' in number:
            tracks = number.split('-')
            if len(tracks) > 2:
                raise SongOrderRangeError(f'Range was entered incorrectly: {number}')
            else:
                for i in range(int(tracks[0]), int(tracks[1]) + 1):
                    new_order.append(i)
        else:
            raise SongOrderError(f'Part of the song order was entered incorrectly: {number}')
    return new_order

def number_of_songs_match(folder, songs):
    """
    Checks if the number of music files in folder matches the number of tracks
    listed in songs.
    
    Arguments:
        - folder: path to folder where music files are found
        - songs: list of track numbers
    Returns:
        True / False
    """
    files = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith('.mp3')]
    
    if len(files) != len(songs):
        return False
    
    return True

def log_function(start_msg=None, end_msg=None, show_time=False, duration_msg='Duration'):
    def log_function_info(func):
        def log_wrapper(*args, **kwargs):
            if start_msg:
                print(f'### {start_msg}')
                
            start = time.time()
            value = func(*args, **kwargs)
            end = time.time()
            
            if show_time:
                print(f'{duration_msg}: {end - start:.2f} seconds')
                
            if end_msg:
                print(end_msg)
            return value
        return log_wrapper
    return log_function_info

def log_sub_function(success_msg=None, failed_msg=None):
    def log_sub_function_info(func):
        def log_sub_wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            
            if value and success_msg:
                print(f'Success: {success_msg}')
            elif not value and failed_msg:
                print(f'Failed: {failed_msg}')
            
            return value
        return log_sub_wrapper
    return log_sub_function_info