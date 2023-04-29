# Module that creates and loads the necessary data for the operation of the program
import json
import os
from datetime import datetime


def read_json():
    """
    Function responsible for creating and reading the .json with the necessary data for the operation of the program.
    :return: Data stored in the configuration .json and a boolean that identifies if the .json was
    successfully read (false) or created (true).
    This boolean variable is used to control the first start of the program.
    """
    try:
        with open('modules/settings/config.json', 'r') as file:
            return json.load(file), False
    except FileNotFoundError:
        # To facilitate the modification of the program parameters, the data is extracted from a plain text file.
        with open("modules/settings/file_path.txt", "r") as file:
            configuration_data = file
            path = configuration_data.readline().rstrip()
            sheet_name = configuration_data.readline()
        month = datetime.now().month

        data = {
            'path': path,
            'sheet_name': sheet_name,
            'last_modified': os.path.getmtime(path),
            'month': month
        }

        with open("modules/settings/config.json", "w") as file:
            json.dump(data, file, indent=4)
        return data, True
