# Module that controls the function call logic of the Google Calendar API
from .create_event import *
from datetime import datetime
from modules.main_files import (xlsx_reader, PKLFile, PKLFileDF)


def reminders():
    data = PKLFileDF("modules/data/data.pkl")
    events_id = {}
    for i in range(len(data.file['NOMBRES'])):
        title = f"Recordatorio de cobro a: {data.file.loc[i, 'NOMBRES']}"
        description = f"Debe pagar: {data.file.loc[i, 'FACTURA']}"
        year = datetime.now().year
        month = datetime.now().month
        day = data.file.loc[i, 'DÍA']
        start = create_iso_date(year=year, month=month, day=day)
        end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
        event_id = create_events(title=title, description=description, start=start, end=end)['id']
        events_id[data.file.loc[i, 'NOMBRES']] = event_id
    events = PKLFile("modules/data/events_id.pkl")
    events.add_item(events_id)


def update_reminders():
    events = PKLFile("modules/data/events_id.pkl")
    old_data = PKLFileDF("modules/data/data.pkl")
    new_data = xlsx_reader(True)

    count = 0
    for name in list(old_data.file['NOMBRES']):
        # We are looking for deleted people
        if name not in list(new_data['NOMBRES']):
            delete_event(events.file[name])
            events.delete_item(name)
        else:
            # Are there changes in the days of reminder?
            if old_data.file.loc[count, 'DÍA'] != new_data.loc[count, 'DÍA']:
                year = datetime.now().year
                month = datetime.now().month
                day = new_data.loc[count, 'DÍA']
                start = create_iso_date(year=year, month=month, day=day)
                end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
                update_event_time(events.file[name], start, end)
            # Are there any changes to the reminder description?
            if old_data.file.loc[count, 'FACTURA'] != new_data.loc[count, 'FACTURA']:
                description = f"Debe pagar: {new_data.loc[count, 'FACTURA']}"
                update_event_description(events.file[name], description)
        count += 1

    # We are looking for added people
    count = 0
    for name in list(new_data['NOMBRES']):
        if name not in list(old_data.file['NOMBRES']):
            title = f"Recordatorio de cobro a: {name}"
            description = f"Debe pagar: {new_data.loc[count, 'FACTURA']}"
            year = datetime.now().year
            month = datetime.now().month
            day = new_data.loc[count, 'DÍA']
            start = create_iso_date(year=year, month=month, day=day)
            end = create_iso_date(year=year, month=month, day=day, hour=12, minute=0)
            event_id = create_events(title=title, description=description, start=start, end=end)['id']
            events.add_item({name: event_id})
        count += 1


def create_iso_date(year, month, day, hour=6, minute=30):
    return debug_day(year, month, day, hour, minute).isoformat()


def debug_day(year, month, day, hour, minute):
    while True:
        # Control dates that exceed the current month.
        try:
            date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            break
        except ValueError:
            day -= 1
    return date
