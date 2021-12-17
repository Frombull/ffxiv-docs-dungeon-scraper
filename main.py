import json
import logging as log

from constants import *
from dungeon_scraper import Dungeons
from google_docs_functions import *


log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

#TODO: Cortar o 'doc_id' de uma url compelta de uma tabela
DOC_ID = '1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI'


def main():
    first_row = get_first_row(id=DOC_ID)
    first_row_map = make_first_row_map(first_row)
    #TODO: first row só que com os nome bunitinho pra ja pegar do json

    # TODO: Formatar o first row range bunitinho com uma função ou sla
    dungeons_read = readFromDocs(id=DOC_ID,
                                 range=f'{first_row_map["dungeon"]}1:{first_row_map["dungeon"]}100')

    # TODO: Jogar isso p uma função e dar um nome bacana
    dungeons_json = {}
    for i, dungeon_row in enumerate(dungeons_read, 1):
        dungeon_name = str(dungeon_row[0])
        dungeon_info = Dungeons.get(dungeon_name)

        if dungeon_info:
            dungeons_json[f'dungeon_{i}'] = dungeon_info
        else:
            dungeons_json[f'dungeon_{i}'] = NONE_DICT

    write_body = []
    row = []
    for dg in dungeons_json:
        for i in range(9):  #TODO: hardcoded 9..
            row.append(dungeons_json[dg][first_row[i]])

        write_body.append(row)
        row = []

    #TODO: Pegar o range necessario e usar uma função p formatar
    writeInDocs(id=DOC_ID,
                range='A1:I12',
                write_body=write_body)


if __name__ == '__main__':
    log.info(f'Running {__file__}')
    main()
