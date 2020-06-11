import datetime
import json
import os
import pickle

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from numpy.random import randint
from decouple import config

# change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = config('SAMPLE_SPREADSHEET_ID_input')
CREDENTIALS_JSON = config("CREDENTIALS_JSON")

# change the range if needed
SAMPLE_RANGE_NAME = "A1:AA1000"


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
Create_Service(
    CREDENTIALS_JSON, "sheets", "v4", ["https://www.googleapis.com/auth/spreadsheets"]
)


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
            body=dict( majorDimension="ROWS", values=payload),
        )
        .execute()
    )
    print("Sheet successfully Updated", response_date)
    return response_date


def create_payload(user_id="000011982", date=1233475435, name="Nina"):
    row = [user_id, date, name,]

    return [row]

def endpoint(event, context):
    """
    Update googledocs
    """
    current_time = datetime.datetime.now().time()

    payload_data = create_payload()

    res = Export_Data_To_Sheets(payload_data)

    body = {"message": "Hello, the current time is " + str(current_time) }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
