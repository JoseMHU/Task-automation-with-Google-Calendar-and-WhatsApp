# Module that regulates the execution or not of the rest of the files
import os
from datetime import datetime
from .file_builder import config_json
from .xlsx_reader import xlsx_reader
from modules.reminders_service import (reminders, update_reminders)
from modules.messenger_service import (update_month, file_update)


def watchful():
    # The status variable is used to control the first start of the program.
    # Moment at which a module execution is forced xlsx_reader to create the main data file (data.pkl)
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
    if config_json.file["month"] != datetime.now().month:
        config_json.file['month'] = datetime.now().month
        config_json.save()
        reminders()
        update_month()
