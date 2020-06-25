#!/source/bin/env python
import pathlib
import yaml
import platform 
import numpy as np


def load_config(config_name):

    # load basic config file
    base_path = pathlib.Path(__file__).resolve().parent.parent

    file_config = base_path.joinpath(config_name)

    with open(file_config) as file_config:
        config_all = yaml.safe_load(file_config)
 
    dropbox_dir = pathlib.Path(config_all[platform.node()]['dropbox_dir'])

    log_dir = dropbox_dir.joinpath( config_all['log_add'][0], 
                                    config_all['log_add'][1]
                                    )
    task_config = dropbox_dir.joinpath( config_all['task_config'][0], 
                                    config_all['task_config'][1],
                                    config_all['task_config'][2]
                                    )
    logo_path = base_path.joinpath( config_all['logo'][0], config_all['logo'][1],)
    fig_dir = base_path.joinpath( config_all['fig'][0] )
    gui_name = base_path.joinpath( config_all['gui'] )

    path_dict = {'base_path': base_path,
                'dropbox':dropbox_dir, 
                'log_dir': log_dir,
                'task_config': task_config,
                'logo_path': logo_path,
                'fig_dir': fig_dir,
                'gui_name': gui_name}

    return path_dict
 

if __name__ == '__main__':

    path_dict = load_config('config.yml')

    print(path_dict)