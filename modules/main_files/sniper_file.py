# Module that regulates the execution or not of the rest of the files
import os
import json
import time
from datetime import datetime
from .config_control import read_json
from .xlsx_reader import xlsx_reader
from modules.reminders_service import (reminders, update_reminders)
from modules.messenger_service import (update_month, file_update)


def watchful():
    config_data, status = read_json()
    # The status variable is used to control the first start of the program.
    # Moment at which a module execution is forced xlsx_reader to create the main data file (data.pkl)
    if status:
        xlsx_reader()
        time.sleep(3)
        reminders()
    elif config_data["last_modified"] != os.path.getmtime(config_data["path"]):
        # We update the .json data
        config_data["last_modified"] = os.path.getmtime(config_data["path"])
        with open('modules/settings/config.json', 'w') as file:
            json.dump(config_data, file, indent=4)
        # We read the file again
        update_reminders()
        xlsx_reader()
        file_update()
    if config_data["month"] != datetime.now().month:
        config_data['month'] = datetime.now().month
        with open('modules/settings/config.json', 'w') as file:
            json.dump(config_data, file, indent=4)
        reminders()
        update_month()
