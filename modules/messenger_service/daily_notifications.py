# This module controls the new feature: daily_notification for sending daily messages to clients.
from .whatsApp_message import message
from .message_status import PKLFileDF


def daily_notifications():
    data = PKLFileDF("modules/data/data.pkl")
    for i in range(len(data.file['DÍA'])):
        name = data.file.loc[i, 'NOMBRES']
        text = f"""¡Hola {name}! Este es un *mensaje automatizado* creado por el equipo de *Saiyan Viking* \n
¿Hoy asistirás al GYM? \n
Confirma tu salida hacía el GYM respondiendo a este mensaje (en caso contrario puedes ignorar este mensaje)\n
Gracias por preferirnos."""
        message(data.file.loc[i, 'NÚMERO'], text)
