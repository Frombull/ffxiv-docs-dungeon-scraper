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


def get_first_row(*, id: str):
    log.info(f'Checking first row of table: {id}')

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range='A1:I1').execute()
    first_row = result.get('values', [])[0]

    if first_row:
        first_row = list(map(str.lower, first_row))
        return first_row
    else:
        log.error('No data found in first row')


def make_first_row_map(row: list) -> dict:
    columns_map = {}
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, item in enumerate(row):
        item = str(item).lower()
        if item in ('dungeon', 'dungeons', 'name', 'names'):
            columns_map.update({'dungeon': letters[i]})
        elif item in ('type', 'types'):
            columns_map.update({'type': letters[i]})
        elif item in ('level', 'levels', 'lvl'):
            columns_map.update({'level': letters[i]})
        elif item in ('ilevel', 'ilevels', 'ilvl', 'itemlevel', 'item-level', 'item_level'):
            columns_map.update({'ilevel': letters[i]})
        elif item in ('expansion', 'expansions'):
            columns_map.update({'expansion': letters[i]})
        elif item in ('patch', 'patches'):
            columns_map.update({'patch': letters[i]})
        elif item in ('difficulty', 'difficulties'):
            columns_map.update({'difficulty': letters[i]})
        elif item in ('party', 'partysize', 'party-size', 'party_size'):
            columns_map.update({'party_size': letters[i]})
        elif item in ('url', 'link', 'wiki'):
            columns_map.update({'url': letters[i]})

    return columns_map
