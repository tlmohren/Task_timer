#!/source/bin/env python
import pathlib
import yaml
import platform
import numpy as np


def load_config(config_name):

    base_path = pathlib.Path(__file__).resolve().parent.parent

    file_config = base_path.joinpath(config_name)

    with open(file_config) as file_config:
        config_all = yaml.safe_load(file_config)

    dropbox_dir = pathlib.Path(config_all[platform.node()]['dropbox_dir'])

    log_dir = dropbox_dir.joinpath(*config_all['log_add'])
    task_config = dropbox_dir.joinpath(*config_all['task_config'])
    dropbox_file = dropbox_dir.joinpath(*config_all['dropbox_file'])

    logo_path = base_path.joinpath(*config_all['logo'])
    fig_dir = base_path.joinpath(*config_all['fig'])
    gui_name = base_path.joinpath(*config_all['gui'])
    gui_main = base_path.joinpath(*config_all['guimain'])

    path_dict = {'base_path': base_path,
                 'dropbox': dropbox_dir,
                 'dropbox_file': dropbox_file,
                 'log_dir': log_dir,
                 'task_config': task_config,
                 'logo_path': logo_path,
                 'fig_dir': fig_dir,
                 'gui_name': gui_name,
                 'gui_main': gui_main}

    cols = np.array([
        [31, 120, 180],
        [178, 223, 138],
        [227, 26, 28],
        [255, 127, 0],
        [202, 178, 214],
        [106, 61, 154],
        [255, 255, 153],
        [51, 160, 44],
        [251, 154, 153],
        [253, 191, 111],
        [166, 206, 227]
    ]) / 255

    path_dict['col'] = cols

    return path_dict


if __name__ == '__main__':

    path_dict = load_config('config.yml')
