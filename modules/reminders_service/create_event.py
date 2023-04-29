# Module that encompasses some of the functions of the Google Calendar API
from .setup import get_calendar_service as gcs


def create_events(title, description, start, end):
    calendar_service = gcs()
    event_id = calendar_service.events().insert(
        calendarId='primary', body={
            "summary": title,
            "description": description,
            "start": {"dateTime": start, "timeZone": 'America/Santo_Domingo'},
            "end": {"dateTime": end, "timeZone": 'America/Santo_Domingo'}
        }).execute()
    return event_id


def delete_event(event_id):
    calendar_service = gcs()
    calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()


def update_event_time(event_id, start, end):
    calendar_service = gcs()
    event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
    event["start"] = {"dateTime": start, "timeZone": 'America/Santo_Domingo'}
    event["end"] = {"dateTime": end, "timeZone": 'America/Santo_Domingo'}
    calendar_service.events().update(calendarId='primary', eventId=event_id, body=event).execute()


def update_event_description(event_id, description):
    calendar_service = gcs()
    event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
    event["description"] = description
    calendar_service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
