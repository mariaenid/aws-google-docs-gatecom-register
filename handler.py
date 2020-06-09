import os
import json
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


"""
google docs link
https://docs.google.com/spreadsheets/d/1V5Cq71O-XPWRqZ0lIsUYEj65LeVUQNHZFG5MhsLuVL0/edit?usp=sharing

"""
import pandas as pd
from numpy.random import randint

columns = ['i','double','square']
rows = []

for i in range(6):
    row = [i, i*2, i*i]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

#change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1V5Cq71O-XPWRqZ0lIsUYEj65LeVUQNHZFG5MhsLuVL0'

#change the range if needed
SAMPLE_RANGE_NAME = 'A1:AA1000'

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)

    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None

# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])


def Export_Data_To_Sheets(gsheetId):
    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated', response_date)


def endpoint(event, context):
    """
    Update googledocs
    """
    current_time = datetime.datetime.now().time()
    Export_Data_To_Sheets(SAMPLE_SPREADSHEET_ID_input)

    body = {
        "message": "Hello, the current time is " + str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
