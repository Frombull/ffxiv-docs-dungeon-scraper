from __future__ import print_function

import logging as log

from googleapiclient.discovery import build

from constants import *

log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

service = build('sheets', 'v4', credentials=CREDS)


def readFromDocs(*, id: str, range: str):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range=range).execute()
    values = result.get('values', [])

    return values if values else log.error('No data found')


def writeInDocs(*, id: str, range: str, write_body: list):
    request = service.spreadsheets().values().update(spreadsheetId=id, range=range,
                                                     valueInputOption="RAW",
                                                     body={"values": write_body})
    response = request.execute()

    return response if response else log.error('No data written')


if __name__ == '__main__':
    # print(readFromDocs(id='1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI',
    #                    range='A1:A1000'))

    test_body = [['test1'],
                 ['test2'],
                 ['test3'],
                 ['test4']]
    writeInDocs(id='1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI',
                range='A1:a1000',
                write_body=test_body)
    pass
