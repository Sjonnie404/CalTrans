import pycronofy
import pprint
pp = pprint.PrettyPrinter(indent=4)

cronofy = pycronofy.Client(access_token="xgoU_7FW_u1-z_x6uHdoG1l0v8KSciuK")

event = {
    'calendar_id': "cal_XP9@Yw7C@wC-6Bjo_xpI@DzAnyq6nxaM9bicguw",
    'event_id': "unique-event-id2",
    'summary': "Board meeting",
    'description': "Discuss plans for the next quarter.",
    'start': "2019-06-15T12:00:00Z",
    'end': "2019-06-15T12:30:00Z",
    'tzid': "Europe/Amsterdam",
    'location': {
        'description': "Board room"
    }
}



cronofy.upsert_event(calendar_id='cal_XP9@Yw7C@wC-6Bjo_xpI@DzAnyq6nxaM9bicguw', event=event)