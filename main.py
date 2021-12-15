import logging as log

from dungeon_scraper import Dungeons
from quickstart import readFromDocs, writeInDocs


log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')


def main():
    dungeons_read = readFromDocs(id='1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI',
                                 range='A1:A100')

    dungeons_json = {}
    for i, dungeon_row in enumerate(dungeons_read, 1):
        dungeon_name = str(dungeon_row[0])
        dungeon_info = Dungeons.get(dungeon_name)
        print(f'[{i}]...')

        dungeons_json[f'dungeon_{i}'] = dungeon_info

    print('-' * 80)

    # print(json.dumps(dungeons_json, indent=2))
    # print('-' * 80)

    write_body = []
    for dg_number in dungeons_json:
        item = [dungeons_json[dg_number]['ilevel']]
        write_body.append(item)

    print(f'write_body = {write_body}')

    writeInDocs(id='1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI',
                range='B1:B1000',
                write_body=write_body)


if __name__ == '__main__':
    log.info(f'Running {__file__}')
    main()
