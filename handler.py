import datetime
import json
import os
import pickle
import requests

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from numpy.random import randint
from decouple import config

# change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = config("SAMPLE_SPREADSHEET_ID_input")
CREDENTIALS_JSON = config("CREDENTIALS_JSON")

# change the range if needed
SAMPLE_RANGE_NAME = "A1:AA1000"

# gatecom database
USERNAME_GATECOM = config("USERNAME_GATECOM")
PASSWORD_CATEGOM = config("PASSWORD_CATEGOM")
URL_GATECOM = config("URL_GATECOM")

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    # print(SCOPES)

    cred = None

    if os.path.exists("token_write.pickle"):
        with open("token_write.pickle", "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open("token_write.pickle", "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, "service created successfully")
        # return service
    except Exception as e:
        print(e)
        # return None


# change 'my_json_file.json' by your downloaded JSON file.
Create_Service(CREDENTIALS_JSON, "sheets", "v4", ["https://www.googleapis.com/auth/spreadsheets"])


def Export_Data_To_Sheets(payload):
    """
    google docs link
    https://docs.google.com/spreadsheets/d/1V5Cq71O-XPWRqZ0lIsUYEj65LeVUQNHZFG5MhsLuVL0/edit?usp=sharing
    """

    print("Writting with payload", payload)
    # add args here
    response_date = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
            valueInputOption="RAW",
            range=SAMPLE_RANGE_NAME,
            body=dict(majorDimension="ROWS", values=payload),
        )
        .execute()
    )
    print("Sheet successfully Updated", response_date)
    return response_date


def create_payload(*args):
    """
    args**
        user_id, current_time, name, device_id, state
    """
    return [[arg for arg in args]]

def get_user(user_id):
    """
    Response**
        {'total_rows': 74,
        'offset': 20,
        'rows': [{'id': 'b788f2f01970b14249fe8506d84c114e',
        'key': '30917B',
        'value': {'name': 'Janina Herrera 2', 'estado': 'autorizado'}}]
        }
    """
    client = requests.Session()
    client.auth = (USERNAME_GATECOM, PASSWORD_CATEGOM)

    url = "%s?key=\"%s\"" % (URL_GATECOM, user_id)
    print("URL gatecommm", url)

    r = client.get(url)
    if r.status_code == 200 and len(r.json()["rows"]) == 1:
        return r.json()["rows"][0].get("value", None) # the first record
    else:
        raise "Can't Find key %s" % user_id

def endpoint(event, context):
    """
    Update googledocs
    """
    user_id = event.get("user_id", None)
    device_id = event.get("device_id", None)
    current_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    if user_id:
        print("Updating access with id {} on {}".format(user_id, device_id))

        try:
            user_gatecom = get_user(user_id)
            name = user_gatecom.get("name", None)
            estado = user_gatecom.get("estado", None)

            # add_args = lambda *k: k
            payload_data = create_payload(user_id, name, device_id, current_time, estado)

            res = Export_Data_To_Sheets(payload_data)
            status = 200
        except Exception as e:
            print("Error %s" % e)
            status = 400

    body = {"message": "Hello, the current time is " + str(current_time)}

    response = {"statusCode": status, "body": json.dumps(body)}

    return response
