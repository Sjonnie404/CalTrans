##################################################################
__Author__ = "Shane Ian Pullens"
__Version__ = 1.0

#TODO:

##################################################################

#####   Imports   #####
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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # this gives the correct rights to edit file.


def getCredentials():
    """ This method
        :param: None
        :return:
        """

    #### Google part
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
    print("Authenticating Google API...")
    try:
        googleAPI = build('calendar', 'v3', credentials=creds)
    except:
        print("Something went wrong with authenticating Google")
    print("Google authenticated succesfully!\n")

    apple_token = ""
    while True:
        if os.path.exists('Data/AppleToken.txt'):
            AppleCreds = open('Data/AppleToken.txt', 'r')
            apple_token = AppleCreds.readline()
            #print(apple_token)
            break
        else:
            AppleCreds = open('Data/AppleToken.txt', 'w')
            print("Acces token? --> See readme!")
            AppleCreds.write(str(input("Please paste your access token string here and press enter.\n")))
            AppleCreds.close()
            print("retrying")


    print("Authenticating Apple API")
    try:
        appleAPI = pycronofy.Client(access_token=apple_token)
    except:
        print("Something went wrong with authenticating Apple")
    print("Apple authenticated succesfully!\n")

    return googleAPI, appleAPI


def conCheck(googleAPI, appleAPI):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print("Testing Google API connection...")
    try:
        googleAPI.events().list(calendarId='primary', timeMin=now,
                                maxResults=1, singleEvents=True,
                                orderBy='startTime').execute()
    except:
        print("An error occurred whilst connecting to the Google API!")
        exit(0)
    print("Google API connection established!\n")

    print("Testing Apple API connection...")
    try:
        appleAPI.read_events().all()
    except:
        print("An error occurred whilst connecting to the Apple API!")
        exit(0)
    print("Apple API connection established!\n")

    return googleAPI, appleAPI

def googlePrep(googleAPI):
    print("Clearing Google calendar...")
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    all_events = googleAPI.events().list(calendarId='primary', timeMin=now).execute()
    events = all_events.get('items', [])
   # print(len(all_events))

   # print(events)

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
       # print(start, event['summary'], event['id'])
        googleAPI.events().delete(calendarId='primary', eventId=event['id']).execute()

    print("Cleared Google calendar succesfully!")
    print("(Clearing takes about 10 seconds to take effect)")
#service.events().delete(calendarId='primary', eventId='eventId').execute()

def appleExtract(appleAPI):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = appleAPI.read_events(from_date=now).all()

    return events

def ApptoGo(events):
    eventList = []
    for event in events:
      #  print(event)
        summary = event['summary']
        description = event['description']
       # start = event['start']
       # print(start)
       # end = event['end']
        start = str(event['start']).replace("Z","+00:00")
        #print(start)
        if len(start) == 10:
            print("changed date format")
            start = start+"T00:01:00+00:00"

        end = str(event['end']).replace("Z", "+00:00")
        if len(end) == 10:
            end = end+"T00:01:00+00:00"

        placeholder = {
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

        eventList.append(placeholder)

    #print(eventList)
    #print(len(eventList))
    return eventList

def googleAdd(eventList, googleAPI):
    print("\nAdding events....")
    for event in eventList:
        #print("adding event")
        #print(event)
        event = googleAPI.events().insert(calendarId='primary', body=event).execute()

    print("Succesfully imported events!")
#    event = service.events().insert(calendarId='primary', body=event).execute()
 #   print('Event created: %s' % (event.get('htmlLink')))




def main():
    apis = getCredentials()  # Checks credentials of user
    checked_apis = conCheck(apis[0], apis[1])  # Check if google and apple connection are working, else throw exception
    googlePrep(checked_apis[0])  # Connects to google and deletes all current events
    events = appleExtract(checked_apis[1])  # Connect to apple and extracts all upcoming events
    eventList = ApptoGo(events)  # Converts Google Json to Apple Json format
    googleAdd(eventList, checked_apis[0])  # Post all google events in calendar


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)  # Sets Pretty Print object.
    os.chdir('..')  # navigates back to parent directory, makes it easier to use different directories
    main()