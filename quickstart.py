import logging as log

from googleapiclient.discovery import build

from constants import *


log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

service = build('sheets', 'v4', credentials=CREDS)


def readFromDocs(*, id: str, range: str):
    log.info(f'Reading from table id: {id}, with range: {range}')

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range=range).execute()
    values = result.get('values', [])

    return values if values else log.error('No data found')


def writeInDocs(*, id: str, range: str, write_body: list):
    log.info(f'Writing in table id: {id}, with range: {range}')

    request = service.spreadsheets().values().update(spreadsheetId=id, range=range,
                                                     valueInputOption="RAW",
                                                     body={"values": write_body})
    response = request.execute()

    return response if response else log.error('No data written')
