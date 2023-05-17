# Main program file
from modules import (watchful, notice, prior_notice)

if __name__ == "__main__":
    # We analyze the changes in the Excel file, and we control the events of the Google calendar.
    daily_notifications = True
    watchful(daily_notifications)

    # We execute the notification and pre-notification modules by WS.
    # A direct call is made to these functions to be able to disable them if necessary.
    notice()
    prior_notice()

