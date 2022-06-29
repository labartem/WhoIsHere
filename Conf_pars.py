import configparser
import os

# Work with config file
def create_conf_file(path):
    config = configparser.ConfigParser()
    config.add_section('APP')
    config.set('APP', 'always_on_top', 'False')
    config.set('APP', 'keylogger', 'False')

    path = path + 'file_config.ini'
    with open(path, 'w') as configfile:
        config.write(configfile)

def read_con_file(path):
    config = configparser.ConfigParser()
    config.read(path+"file_config.ini")
    a = config.items('APP')
    return config.items('APP')

def save_config_file(path, value):
    config = configparser.ConfigParser()
    path = path + 'file_config.ini'
    config.read(path)
    print(path)
    print("Save config " ,value[0], value[1])
    config.set('APP', 'always_on_top', str(value[0]))
    config.set('APP', 'keylogger', str(value[1]))

    with open(path, 'w') as configfile:
        config.write(configfile)
