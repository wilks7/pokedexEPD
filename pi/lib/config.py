import os
import configparser

def get_config(section, value):
    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, 'omni-epd.ini')
    file_parser = configparser.ConfigParser()
    file_parser.read(config_file)

    try:
        return file_parser.get(section, value)
    except:
        return None

