# Module that controls the function call logic of the Google Calendar API
from .create_event import *
import pickle
from datetime import datetime
from modules.main_files import xlsx_reader


def reminders():
    """
    Function in charge of creating the reminders of the month. It only runs when the month changes or when the program
    is launched for the first time.
    """
    with open("modules/data/data.pkl", "rb") as file:
        data = pickle.load(file)
    events_id = {}
    for i in range(len(data['NOMBRES'])):
        title = f"Recordatorio de cobro a: {data.loc[i, 'NOMBRES']}"
        description = f"Debe pagar: {data.loc[i, 'FACTURA']}"
        year = datetime.now().year
        month = datetime.now().month
        day = data.loc[i, 'DÍA']
        start = create_iso_date(year=year, month=month, day=day)
        end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
        event_id = create_events(title=title, description=description, start=start, end=end)['id']
        events_id[data.loc[i, 'NOMBRES']] = event_id
    with open("modules/data/events_id.pkl", "wb") as file:
        pickle.dump(events_id, file)


def create_iso_date(year, month, day, hour=6, minute=30):
    """
    Function that converts the time parameters in ISO format for the Google API.
    :return: Date in ISO format.
    """
    while True:
        # Control dates that exceed the current month.
        try:
            date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            break
        except ValueError:
            day -= 1
    return date.isoformat()


def update_reminders():
    with open("modules/data/events_id.pkl", "rb") as file:
        events_id = pickle.load(file)
    with open("modules/data/data.pkl", "rb") as file:
        old_data = pickle.load(file)
    new_data = xlsx_reader(True)

    count = 0
    for name in old_data['NOMBRES']:
        # We are looking for deleted people
        if name not in new_data['NOMBRES']:
            delete_event(events_id[name])
            del events_id[name]
        else:
            # Are there changes in the days of reminder?
            if old_data.loc[count, 'DÍA'] != new_data.loc[count, 'DÍA']:
                year = datetime.now().year
                month = datetime.now().month
                day = new_data.loc[count, 'DÍA']
                start = create_iso_date(year=year, month=month, day=day)
                end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
                update_event_time(events_id[name], start, end)
            # Are there any changes to the reminder description?
            elif old_data.loc[count, 'FACTURA'] != new_data.loc[count, 'FACTURA']:
                description = f"Debe pagar: {new_data.loc[count, 'FACTURA']}"
                update_event_description(events_id[name], description)
        count += 1

    # We are looking for added people
    count = 0
    for name in new_data['NOMBRES']:
        if name not in old_data['NOMBRES']:
            title = f"Recordatorio de cobro a: {name}"
            description = f"Debe pagar: {new_data.loc[count, 'FACTURA']}"
            year = datetime.now().year
            month = datetime.now().month
            day = new_data.loc[count, 'DÍA']
            start = create_iso_date(year=year, month=month, day=day)
            end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
            event_id = create_events(title=title, description=description, start=start, end=end)['id']
            events_id[name] = event_id
        count += 1

    with open("modules/data/events_id.pkl", "wb") as file:
        pickle.dump(events_id, file)
