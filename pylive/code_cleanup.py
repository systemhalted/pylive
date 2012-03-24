#! /usr/bin/env python
"""
    This is a script to clean the code produced by the user.
    This program will be executed as cronjob
"""
from constants import tmp
from time import ctime
from os.path import getmtime, isfile, sep
from os import listdir, remove

def get_a_filename():
    """ Function returns file by file in tmp directory"""
    for filename in listdir(tmp):
        yield sep.join([tmp, filename])

def delete_file(filename):
    """ 
       function to delete files.
       will update the text , so lazy, 3.09AM while writing this
    """
    cur_time = ctime()
    days = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    if isfile(filename):
        modified_time = ctime(getmtime(filename))
        cur_time_split = cur_time.split(' ')
        modified_time_split = modified_time.split(' ')
        if days[cur_time[:3]] > days[modified_time[:3]]:
            remove(filename)
            with open('code_cleanup.txt', 'a') as f:
                msg = ' '.join([filename, "was removed at ", ctime(), "\n"])
                f.write(msg)
        else:
            if cur_time_split[3].split(':')[1] > \
                modified_time_split[3].split(':')[1] > 2:
                remove(filename)
                with open('code_cleanup.txt', 'a') as f:
                    msg = ' '.join([filename, "was removed at ", ctime(), "\n"])
                    f.write(msg)

           
        
if __name__ == "__main__":
    try:
        for filename in get_a_filename():
            delete_file(filename)
    except Exception as e:
        with open('code_cleanup_error.log', "a") as f:
            f.write(e.message + "\n")

