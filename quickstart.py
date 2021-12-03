from __future__ import print_function

import logging as log
from pprint import pprint

import googleapiclient.errors
from google.oauth2 import service_account
from googleapiclient.discovery import build


log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'top_secret_keys.json'
CREDS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = '1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI'
SAMPLE_RANGE = 'A1'

service = build('sheets', 'v4', credentials=CREDS)


def readFromDocs():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SAMPLE_RANGE).execute()
    values = result.get('values', [])

    return values if values else log.error('No data found')


def writeInDocs():
    test_body = [['test1', 'test2'],
                 ['test3', 'test4']]

    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE,
                                                     valueInputOption="RAW",
                                                     body={"values": test_body})
    response = request.execute()

    return response if response else log.error('No data written')


if __name__ == '__main__':
    # readFromDocs()
    # writeInDocs()
    pass
