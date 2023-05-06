# Module that controls the sending of messages
import pickle
from datetime import datetime
from .whatsApp_message import message
from modules.main_files import (PKLFile, JsonFile, PKLFileDF)
from modules.reminders_service import debug_day


class Notifications(PKLFile):
    def __init__(self, path):
        PKLFile.__init__(self, path)

    def add_item(self, key: str):
        self.file[key] = False
        with open(self._path, "wb") as file:
            pickle.dump(self.file, file)

    def reboot(self, keys: list):
        del self.file
        self.file = {}
        for i in keys:
            self.file[i] = False
        with open(self._path, "wb") as file:
            pickle.dump(self.file, file)

    def change_status(self, key: str):
        try:
            if self.file[key]:
                self.file[key] = False
            else:
                self.file[key] = True
            with open(self._path, "wb") as file:
                pickle.dump(self.file, file)
        except KeyError:
            self.file[key] = True
            with open(self._path, "wb") as file:
                pickle.dump(self.file, file)


class PriorNotifications(Notifications):
    def __init__(self, path):
        Notifications.__init__(self, path)

    def add_item(self, key: str):
        self.file[key] = True
        with open(self._path, "wb") as file:
            pickle.dump(self.file, file)

    def reboot(self, keys: list):
        del self.file
        self.file = {}
        for i in keys:
            self.file[i] = True
        with open(self._path, "wb") as file:
            pickle.dump(self.file, file)


def prior_notice():
    data = PKLFileDF("modules/data/data.pkl")
    month = JsonFile('modules/settings/config.json').file['month']
    now = datetime.now()
    prior_notifications = PriorNotifications("modules/data/prior_notifications.pkl")
    debug_notification(data.file['NOMBRES'], prior_notifications)

    for i in range(len(data.file['DÍA'])):
        day = data.file.loc[i, 'DÍA']
        date_for_collection = debug_day(year=datetime.now().year, month=month, day=day, hour=23, minute=59)
        if (0 < (date_for_collection - now).days <= 7 or (date_for_collection - now).days <= -24) \
                and not prior_notifications.file[data.file.loc[i, 'NOMBRES']]:
            # We personalize the message
            name = data.file.loc[i, 'NOMBRES']
            precio = data.file.loc[i, 'FACTURA']
            text = f"""¡Hola {name}! Este es un *mensaje automatizado* creado por el equipo de *Saiyan Vikingo* \n
Para recordarte que dentro de una semana deberás pagar un monto de *{precio}* $DOP 
por los servicios del presente mes. \n
Gracias por preferirnos.\n
_No es necesario que responda a este mensaje._ """
            message(data.file.loc[i, 'NÚMERO'], text)
            prior_notifications.change_status(data.file.loc[i, 'NOMBRES'])


def notice():
    data = PKLFileDF("modules/data/data.pkl")
    month = JsonFile('modules/settings/config.json').file['month']
    now = datetime.now()

    prior_notifications = PriorNotifications("modules/data/prior_notifications.pkl")
    notifications = Notifications("modules/data/notifications.pkl")
    debug_notification(data.file['NOMBRES'], prior_notifications, notifications)

    for i in range(len(data.file['DÍA'])):
        day = data.file.loc[i, 'DÍA']
        date_for_collection = debug_day(year=datetime.now().year, month=month, day=day, hour=23, minute=59)
        if (date_for_collection - now).days == 0 and not notifications.file[data.file.loc[i, 'NOMBRES']]:
            # We personalize the message
            name = data.file.loc[i, 'NOMBRES']
            precio = data.file.loc[i, 'FACTURA']
            text = f"""¡Hola {name}! Este es un *mensaje automatizado* creado por el equipo de *Saiyan Vikingo* \n
Para recordarte que hoy deberás pagar un monto de *{precio}* $DOP \n
por los servicios del presente mes. \n
Gracias por preferirnos.\n
_No es necesario que responda a este mensaje._ """
            message(data.file.loc[i, 'NÚMERO'], text)
            notifications.change_status(data.file.loc[i, 'NOMBRES'])
            # Pre-notification for the next month is enabled (3 weeks in practical terms).
            prior_notifications.change_status(data.file.loc[i, 'NOMBRES'])


def update_month():
    """
    Updates the notification log when the month changes
    """
    data = PKLFile("modules/data/data.pkl")
    notifications = Notifications("modules/data/notifications.pkl")
    notifications.reboot(data.file['NOMBRES'])


def file_update():
    data = PKLFile("modules/data/data.pkl")

    prior_notifications = PriorNotifications("modules/data/prior_notifications.pkl")
    notifications = Notifications("modules/data/notifications.pkl")
    debug_notification(data.file['NOMBRES'], prior_notifications, notifications)

    # Add new records
    for name in data.file['NOMBRES']:
        if name not in notifications.file:
            notifications.add_item(name)
            prior_notifications.add_item(name)

    # Delete records
    list_del = []
    for name in notifications.file:
        if name not in list(data.file['NOMBRES']):
            list_del.append(name)
    for i in list_del:
        notifications.delete_item(i)
        prior_notifications.delete_item(i)
    del list_del


def debug_notification(data: list, *notifications: Notifications):
    for item in notifications:
        if not item.found:
            item.reboot(data)
