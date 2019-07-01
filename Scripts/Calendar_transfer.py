##################################################################
__Author__ = "Shane Ian Pullens"
__Version__ = 1.0

# TODO: Fix Google's warning
# TODO: Add documentation
# TODO: Remove the Cronify wrapper and use the core icloud API
# TODO: !!Look for a way to not hard copy paste whole calendar but obly add new events and edit changed events!!
# TODO: Check try excepts
# TODO: Look for deploy possibilities [phone app?, web app, Compiler?]
# TODO: Fix Bug: Apple now takes whole day, whilst google takes exact time. (or maybe the other way around)
# TODO: Beschrijving:Check if ID changes when info is changed (changed note, changes time & change date)  For both Apple & Google
#
# TODO Newer version: controller for differences in Timezone
#
# TODO Method: checkChanges: Save list of event IDs, if there are new id's in the new fetched list update. Update the lists, else go further

##################################################################

# ~~~ Imports ~~~
# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# Apple-Cronofy API
import pycronofy
# Additional
import pprint
import os
import pickle
import os.path
import datetime

pp = pprint.PrettyPrinter(indent=4)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # this gives the correct rights to edit file for google API


def getCredentials():
    """ This method checks if the user had logged into google calendar and apple icloud, if not it prompts the user and
        and saves the credentials.
        :param: None
        :return: Google API object
        :return: Apple API object
        """

    #  Google part
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

    print("Authenticating Google API...")  # Test if the Google API doesn't trow an error
    try:
        googleAPI = build('calendar', 'v3', credentials=creds)  # Generates google API object
    except:
        print("Something went wrong with authenticating Google")
    print("Google authenticated succesfully!\n")

    while True:
        if os.path.exists('Data/AppleToken.txt'):  # Checks if the user has added the cronify api token
            AppleCreds = open('Data/AppleToken.txt', 'r')
            apple_token = AppleCreds.readline()
            break
        else:  # If file doesn't exist ask the user for the token and save it in Data/AppleToken.txt and check again
            AppleCreds = open('Data/AppleToken.txt', 'w')
            print("Acces token? --> See readme!")
            AppleCreds.write(str(input("Please paste your access token string here and press enter.\n")))
            AppleCreds.close()
            print("retrying")

    print("Authenticating Apple API")  # Test if the Apple API doesn't trow an error
    try:
        appleAPI = pycronofy.Client(access_token=apple_token)  # Generates cronofy (apple) API object
    except:
        print("Something went wrong with authenticating Apple")
    print("Apple authenticated succesfully!\n")

    return googleAPI, appleAPI


def conCheck(googleAPI, appleAPI):
    """     This method (Connection check) checks if both APIs gen retrieve data from them before doing any
            other operations
    :param googleAPI: Google API object
    :param appleAPI:  Apple API object
    :return: Checked Google API object
    :return: Checked Apple API object
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    print("Testing Google API connection...")
    try:
        # Fetches a list of of the first upcoming calendar events.
        googleAPI.events().list(calendarId='primary', timeMin=now,
                                maxResults=1, singleEvents=True,
                                orderBy='startTime').execute()
    except:
        print("An error occurred whilst connecting to the Google API!")
        exit(0)  # if the API doesn't work exit the program
    print("Google API connection established!\n")

    print("Testing Apple API connection...")
    try:
        # Fetches a list of all the calendar events
        appleAPI.read_events().all()
    except:
        print("An error occurred whilst connecting to the Apple API!")
        exit(0)  # if the API doesn't work exit the program
    print("Apple API connection established!\n")

    return googleAPI, appleAPI


def googlePrep(googleAPI):
    """     This method prepares the Google calendar for a clean import by removing all events to prevent
            duplicate events.
    :param googleAPI: Google API object
    :return: None
    """
    print("Clearing Google calendar...")
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # Fetches all upcoming Google calendar events
    all_events = googleAPI.events().list(calendarId='primary', timeMin=now).execute()
    events = all_events.get('items', [])  # Add all events dictionaries out of API object

    if not events:  # If there is are no events print this.
        print('No upcoming events found.')

    for event in events:
        # Deletes all fetched  events from google calendar.
        googleAPI.events().delete(calendarId='primary', eventId=event['id']).execute()

    print("Cleared Google calendar succesfully!")
    print("(Clearing takes about 10 seconds to take visual effect)")  # Deleted events take a few seconds to take affect.


def appleExtract(appleAPI):
    """     This method fetches all the events from the Apple calender
    :param appleAPI: Apple API Object
    :return: Returns list of dictionaries that contain an event each.
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = appleAPI.read_events(from_date=now).all()  # Gets all events from the Apple calendar starting from now.

    return events


def ApptoGo(events):
    """    This method converts the Apple syntax to google syntax
    :param events: a list of all the apple events to be imported into the Google calendar
    :return: returns a list of Google-like syntax events.
    """
    eventList = []
    for event in events:
        summary = event['summary']
        description = event['description']

        start = str(event['start']).replace("Z","+00:00")  # Changes the DateTime format from Apple to Google
        if len(start) == 10:  # Apple changes DateTime format when events are planned on days.
            start = start+"T00:01:00+00:00"

        end = str(event['end']).replace("Z", "+00:00")
        if len(end) == 10:
            end = end+"T00:01:00+00:00"

        placeholder = {  # Body of the Google API event
            'summary': summary,
            'location': '',
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': "UTC"
            },
            'end': {
                'dateTime': end,
                'timeZone': "UTC"
            },
            'event': {
                "background": 'blue'
            }
        }

        eventList.append(placeholder)  # Adds event to the event list

    return eventList


def googleAdd(eventList, googleAPI):
    """     This method adds all the events from the event list to the Google calendar
    :param eventList:  List of all the transformed Google-like events
    :param googleAPI:  Google API object
    :return: None
    """
    print("\nAdding events....")
    for event in eventList:
        googleAPI.events().insert(calendarId='primary', body=event).execute()

    print("Successfully imported events!")

# def Testing(googleAPI, appleAPI):
#     now = datetime.datetime.utcnow().isoformat() + 'Z'
#
#     calender = googleAPI.events().list(calendarId='primary', timeMin=now,
#                             maxResults=2, singleEvents=True,
#                             orderBy='startTime').execute()
#     pp.pprint(calender)
#     print()
#
#     for event in calender.get('items'):
#         # Learned that event in this case is the calendar and the item is a event in the calendar, needs further investigation with multiple events!!
#         print("Etag calendar:\t", calender['etag'])
#         print("Etag event:\t\t", event['etag'])
#         print("iCalUID event:\t", event['iCalUID'])
#         print("id event:\t\t", event['id'])


def main():
    """ Main Method
    :return: None
    """
    apis = getCredentials()  # Checks credentials of user
    checked_apis = conCheck(apis[0], apis[1])  # Check if google and apple connection are working, else throw exception
   # print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~` Testing Zone ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    #Testing(apis[0], apis[1])
    googlePrep(checked_apis[0])  # Connects to google and deletes all current events
    events = appleExtract(checked_apis[1])  # Connect to apple and extracts all upcoming events
    eventList = ApptoGo(events)  # Converts Google Json to Apple Json format
    googleAdd(eventList, checked_apis[0])  # Post all google events in calendar


if __name__ == '__main__':
    os.chdir('..')  # navigates back to parent directory, makes it easier to use different directories
    main()
