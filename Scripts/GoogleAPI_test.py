# Testing Googles Calendar API, mainly focused on plasing events
key="AIzaSyB3QGqbWvg8GuDixEt5sI9u3xdgiMrduuU"

client_id =     "753473240940-d0ck0r6qb045e8netqdis0dim7v6s3p1.apps.googleusercontent.com"
client_secret = "C2EQTRbJhIUeoT3DdFTdUyHS"

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os







# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('Data/token.pickle'):
        with open('Data/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Data/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('Data/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # event = {
    #     'summary': 'Test_05',
    #     'location': '',
    #     'description': 'Testing all the stuf',
    #     'start': {
    #         'dateTime': '2019-06-10T09:00:00',  #YYY-mm-dd than 'T' than hh:mm:ss than - than hh:mm last is duration see https://tools.ietf.org/html/rfc3339#section-5.8
    #         'timeZone': 'Europe/Amsterdam',
    #     },
    #     'end': {
    #         'dateTime': '2019-06-10T17:00:00',
    #         'timeZone': 'Europe/Amsterdam',
    #     },
    # }
    #
    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print('Event created: %s' % (event.get('htmlLink')))


    #
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 1 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    print(events_result)
    # print("\n~~~~~~~~~~~~~~~~~~~~~\n")
    #
    # service
    # exit()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

if __name__ == '__main__':
    os.chdir('..')
    main()