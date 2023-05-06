# Module that regulates the execution or not of the rest of the files
import os
from datetime import date
from datetime import datetime
from .file_builder import config_json
from .xlsx_reader import xlsx_reader
from modules.reminders_service import (reminders, update_reminders)
from modules.messenger_service import (update_month, file_update, daily_notifications)


def watchful(daily: bool):
    # The status variable is used to control the first start of the program.
    # Moment at which a module execution is forced xlsx_reader to create the main data file (data.pkl)
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    if not config_json.found:
        xlsx_reader()
        reminders()
    elif config_json.file["last_modified"] != os.path.getmtime(config_json.file["path"]):
        # We update the .json data
        config_json.file["last_modified"] = os.path.getmtime(config_json.file["path"])
        config_json.save()
        # We read the file again
        update_reminders()
        xlsx_reader()
        file_update()
    if config_json.file["month"] != month:
        config_json.file['month'] = month
        config_json.file['day'] = day
        config_json.save()
        reminders()
        update_month()
        if daily and date(year, month, day).weekday() not in [5, 6]:
            # Control of the activation of the function from main
            daily_notifications()
    elif config_json.file['day'] != day:
        config_json.file['day'] = day
        config_json.save()
        if daily and date(year, month, day).weekday() not in [5, 6]:
            # Control of the activation of the function from main
            daily_notifications()
