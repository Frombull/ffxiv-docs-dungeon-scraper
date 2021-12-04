import json
import logging as log
from pprint import pprint

import requests
from bs4 import BeautifulSoup

log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')

log.info('Stating scraper')


class DungeonScraper:
    def __init__(self):
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

    def getDungeon(self, dg_name: str):
        dg_name_filtered = self._filterDgName(dg_name)
        url = 'https://ffxiv.consolegameswiki.com/wiki/' + dg_name_filtered
        log.info(f'Getting dungeon: {dg_name}, with url: {url}')

        r = requests.get(url=url, headers=self.HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')

        infobox = soup.find('div', class_='infobox-n duty')
        dg_name = infobox.find('p', class_='heading').text.strip()

        wrappers = infobox.find('div', class_='wrapper')
        wrapper_1 = list(wrappers.find_all('dl')[0])
        wrapper_2 = list(wrappers.find_all('dl')[1])

        wrapper_1 = list(filter(lambda x: len(str(x)) > 4, wrapper_1))
        wrapper_2 = list(filter(lambda x: len(str(x)) > 4, wrapper_2))


        for i, item in enumerate(wrapper_1):
            # print(f'{i}, {item}')
            if '>difficulty<' in str(item).strip().lower():
                next_item = str(wrapper_1[i+1])
                dg_difficulty = self._filterTags(next_item)
            elif '>level<' in str(item).strip().lower():
                next_item = str(wrapper_1[i + 1])
                dg_level = self._filterTags(next_item)
            elif '>ilevel<' in str(item).strip().lower():
                next_item = str(wrapper_1[i + 1])
                dg_ilevel = self._filterTags(next_item)


        foo = '-'
        return {
            "name": dg_name,
            "type": foo,
            "expansion": foo,
            "level": dg_level,
            "ilevel": dg_ilevel,
            "dificulty": dg_difficulty,
            "partySize": foo,
        }

    @staticmethod
    def _filterDgName(dg_name: str) -> str:
        #log.info('Filtering dungeon name')
        return dg_name.strip().replace(' ', '_')

    @staticmethod
    def _filterTags(item: str) -> str:
        # log.info('Filtering item tags')
        return item[1:].split('<')[0].split('>')[1].replace('\xa0', '')

    @staticmethod
    def _getExpansionFromPatch(patch: str) -> str:  # 2.0
        patches = {
            "2": "A Realm Reborn",
            "3": "Heavensward",
            "4": "Stormblood",
            "5": "Shadowbringers",
            "6": "Endwalker"
        }
        return patches[patch.split('.')[0]]


if __name__ == '__main__':
    potato = DungeonScraper().getDungeon('The Drowned City of Skalla')
    pprint(potato)
