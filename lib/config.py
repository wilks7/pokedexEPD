import os
import configparser

def get_config(section, value):
    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, 'config.ini')
    file_parser = configparser.ConfigParser()
    file_parser.read(config_file)

    return file_parser.get(section, value)