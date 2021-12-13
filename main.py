from dungeon_scraper import Dungeons
from quickstart import readFromDocs, writeInDocs


test_body = [['test1'],
             ['test2'],
             ['test3'],
             ['test4']]


def main():
    dungeons = readFromDocs(id='1iAC6O-_9YSG47CYiTWTvMNL4Li-EaEjuNUZOHgkS4lI',
                            range='A1:A100')

    for dungeon_row in dungeons:
        dungeon = str(dungeon_row[0])
        print(Dungeons.get(dungeon))


if __name__ == '__main__':
    main()
