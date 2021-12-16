import json
import logging as log

from constants import *
from dungeon_scraper import Dungeons
from google_docs_functions import *

log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

DOC_ID = '1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI'


def main():

    fist_row = get_first_row(id=DOC_ID)[0]
    first_row_map = make_first_row_map(fist_row)
    #print(filtered_first_row)


    dungeons_read = readFromDocs(id=DOC_ID,
                                 range=f'{first_row_map["name"]}1:{first_row_map["name"]}100')

    dungeons_json = {}
    for i, dungeon_row in enumerate(dungeons_read, 1):
        dungeon_name = str(dungeon_row[0])
        dungeon_info = Dungeons.get(dungeon_name)

        if dungeon_info:
            print(f'[{i}]...')
            dungeons_json[f'dungeon_{i}'] = dungeon_info
        else:
            print(f'[{i}]xxx')
            dungeons_json[f'dungeon_{i}'] = NONE_DICT

    print(json.dumps(dungeons_json, indent=2))

    # write_body = []
    # for dg_number in dungeons_json:
    #     item = [dungeons_json[dg_number]['ilevel']]
    #     write_body.append(item)
    #
    # print(f'write_body = {write_body}')
    #
    # writeInDocs(id=DOC_ID,
    #             range='B1:B100',
    #             write_body=write_body)


if __name__ == '__main__':
    log.info(f'Running {__file__}')
    main()
