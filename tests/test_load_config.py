import context
import pytest

import platform 

import pathlib 
import task_timer.load_config as lc  


def test_load_config():
    path_dict = lc.load_config('config.yml')
  
    if platform.node() == 'thomas-HP-ZBook-14':
        assert( path_dict['task_config'] == 
            pathlib.Path('/home/thomas/Dropbox/Notebook/miscellaneous/task_timer_config.json') )

if __name__ == '__main__':


    test_load_config()
    print('ran all tests')

