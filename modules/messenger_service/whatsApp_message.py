# Module that handles whatsapp messaging
import pywhatkit


def message(num, text):
    phone_no = "+" + str(num)
    pywhatkit.sendwhatmsg_instantly(phone_no=phone_no, message=text, tab_close=True)
