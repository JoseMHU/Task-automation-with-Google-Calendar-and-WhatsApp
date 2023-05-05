# Module that controls the sending of messages
import pickle
from datetime import datetime
import json
from .whatsApp_message import message


def prior_notice():
    """
    Prior notification (one week before the collection day). It only works after sending a billing notification,
    that is, one month after the launch of the program.
    """
    with open("modules/data/data.pkl", "rb") as file:
        data = pickle.load(file)
    with open('modules/settings/config.json', 'r') as file:
        month = json.load(file)['month']
    now = datetime.now()
    try:
        with open("modules/data/prior_notifications.pkl", "rb") as file:
            prior_notifications = pickle.load(file)
    except FileNotFoundError:
        prior_notifications = {}
        for i in data['NOMBRES']:
            # If the file does not exist, the entire history is loaded as "already sent". In this way, duplication in
            # the sending of prior notifications is avoided. The sending of notifications enables the sending of
            # previous notifications.
            prior_notifications[i] = True

    for i in range(len(data['DÍA'])):
        # When creating datetime objects without time, the day is set to 00:00:00. So for practical purposes, when
        # checking if the stored day and the current day are the same, the result instead of being 0 is -1. So 24h
        # is added to the reading to get 0 in the readings.
        day = data.loc[i, 'DÍA'] + 1
        while True:
            # Control dates that exceed the current month.
            try:
                date_for_collection = datetime(year=datetime.now().year, month=month, day=day)
                break
            except ValueError:
                day -= 1
        if (date_for_collection - now).days <= -24:
            # If 3 weeks have already passed since the reading, the month is changed to validate if a prior
            # notification should be sent.
            date_for_collection = datetime(year=datetime.now().year, month=(month + 1), day=day)
        if 0 < (date_for_collection - now).days <= 7 and not prior_notifications[data.loc[i, 'NOMBRES']]:
            # We personalize the message
            name = data.loc[i, 'NOMBRES']
            precio = data.loc[i, 'FACTURA']
            text = f"""¡Hola {name}! Este es un *mensaje automatizado* creado por el equipo de *Saiyan Vikingo* \n
Para recordarte que dentro de una semana deberás pagar un monto de *{precio}* $DOP 
por los servicios del presente mes. \n
Gracias por preferirnos.\n
_No es necesario que responda a este mensaje._ """
            message(data.loc[i, 'NÚMERO'], text)
            prior_notifications[data.loc[i, 'NOMBRES']] = True

    # We record the sending of the message
    with open("modules/data/prior_notifications.pkl", "wb") as file:
        pickle.dump(prior_notifications, file)


def notice():
    """
    Main notifications by WS about the payment the same day that it must be made
    """
    with open("modules/data/data.pkl", "rb") as file:
        data = pickle.load(file)
    with open('modules/settings/config.json', 'r') as file:
        month = json.load(file)['month']
    now = datetime.now()

    try:
        with open("modules/data/notifications.pkl", "rb") as file:
            notifications = pickle.load(file)
    except FileNotFoundError:
        notifications = {}
        for i in data['NOMBRES']:
            notifications[i] = False

    try:
        with open("modules/data/prior_notifications.pkl", "rb") as file:
            prior_notifications = pickle.load(file)
    except FileNotFoundError:
        prior_notifications = {}
        for i in data['NOMBRES']:
            prior_notifications[i] = True

    for i in range(len(data['DÍA'])):
        day = data.loc[i, 'DÍA'] + 1
        while True:
            try:
                date_for_collection = datetime(year=datetime.now().year, month=month, day=day)
                break
            except ValueError:
                day -= 1
        if (date_for_collection - now).days == 0 and not notifications[data.loc[i, 'NOMBRES']]:
            # We personalize the message
            name = data.loc[i, 'NOMBRES']
            precio = data.loc[i, 'FACTURA']
            text = f"""¡Hola {name}! Este es un *mensaje automatizado* creado por el equipo de *Saiyan Vikingo* \n
Para recordarte que hoy deberás pagar un monto de *{precio}* $DOP \n
por los servicios del presente mes. \n
Gracias por preferirnos.\n
_No es necesario que responda a este mensaje._ """
            message(data.loc[i, 'NÚMERO'], text)
            notifications[data.loc[i, 'NOMBRES']] = True
            # Pre-notification for the next month is enabled (3 weeks in practical terms).
            prior_notifications[data.loc[i, 'NOMBRES']] = False

    # We record the sending of the message
    with open("modules/data/notifications.pkl", "wb") as file:
        pickle.dump(notifications, file)
    # We enable the sending of prior notifications
    with open("modules/data/prior_notifications.pkl", "wb") as file:
        pickle.dump(prior_notifications, file)


def update_month():
    """
    Updates the notification log when the month changes
    """
    with open("modules/data/data.pkl", "rb") as file:
        data = pickle.load(file)
    notifications = {}
    for i in data['NOMBRES']:
        notifications[i] = False
    with open("modules/data/notifications.pkl", "wb") as file:
        pickle.dump(notifications, file)


def file_update():
    with open("modules/data/data.pkl", "rb") as file:
        data = pickle.load(file)

    try:
        with open("modules/data/notifications.pkl", "rb") as file:
            notifications = pickle.load(file)
    except FileNotFoundError:
        notifications = {}
        for i in data['NOMBRES']:
            notifications[i] = False

    try:
        with open("modules/data/prior_notifications.pkl", "rb") as file:
            prior_notifications = pickle.load(file)
    except FileNotFoundError:
        prior_notifications = {}
        for i in data['NOMBRES']:
            prior_notifications[i] = True

    # Add new records
    for name in data['NOMBRES']:
        if name not in notifications.keys():
            notifications[name] = False
            prior_notifications[name] = True

    # Delete records
    list_del = []
    for name in notifications:
        if name not in list(data['NOMBRES']):
            list_del.append(name)
    for i in list_del:
        notifications.pop(i)
        prior_notifications.pop(i)
    del list_del

    with open("modules/data/notifications.pkl", "wb") as file:
        pickle.dump(notifications, file)

    with open("modules/data/prior_notifications.pkl", "wb") as file:
        pickle.dump(prior_notifications, file)
