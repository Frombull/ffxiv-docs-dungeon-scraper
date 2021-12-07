import logging as log
from pprint import pprint
import json

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
        URL = f'https://ffxiv.consolegameswiki.com/wiki/{dg_name_filtered}'

        log.info(f'Getting dungeon: {dg_name}, from url: {URL}')

        r = requests.get(url=URL, headers=self.HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')

        infobox = soup.find('div', class_='infobox-n duty')
        dg_name = infobox.find('p', class_='heading').text.strip()

        wrappers = infobox.find('div', class_='wrapper').find_all('dl')

        wrapper_final = []
        for wrapper in wrappers:
            for i, item in enumerate(wrapper):
                if len(str(item)) > 4:
                    wrapper_final.append(str(item).strip().lower())

        for i, item in enumerate(wrapper_final):
            next_index = i+1
            if next_index >= len(wrapper_final):
                break

            next_item = wrapper_final[next_index]
            if '>difficulty<' in item:
                dg_difficulty = self._filterTags(next_item)
            elif '>level<' in item:
                dg_level = self._filterTags(next_item)
            elif '>ilevel<' in item:
                dg_ilevel = self._filterTags(next_item)
            elif '>patch<' in item:
                dg_patch = next_item.split('</a>')[0].split('">')[1]
                dg_expansion = self._getExpansionFromPatch(dg_patch)
            elif '>party size<' in item:
                if 'Alliance' in next_item:
                    dg_party_size = 'Alliance'
                else:
                    dg_party_size = self._filterTags(next_item)
                    dg_party_size = (dg_party_size.split('Party')[0] + 'Party').title()


        main_page = soup.find('div', class_='mw-parser-output')
        for p in main_page.find_all('p'):
            if 'href="/wiki/Dungeon"' in str(p):
                dg_type = 'Dungeon'
            elif 'href="/wiki/Trial"' in str(p):
                dg_type = 'Trial'
            elif 'href="/wiki/Raid"' in str(p):
                dg_type = 'Raid'

        # TODO: Set everything as None by default
        return {
            "name": dg_name,
            "type": dg_type,
            "level": dg_level,
            "ilevel": dg_ilevel,
            "expansion": dg_expansion,
            "patch": dg_patch,
            "dificulty": dg_difficulty,
            "partySize": dg_party_size,
            "url": URL
        }

    @staticmethod
    def _filterDgName(dg_name: str) -> str:
        log.info(f'Filtering dungeon name: {dg_name}')
        return dg_name.strip().replace(' ', '_').replace("'", '%27').title()

    @staticmethod
    def _filterTags(item: str) -> str:
        # log.info('Filtering item tags')
        try:
            return item[1:].split('<')[0].split('>')[1].replace('\xa0', '').title()
        except IndexError:
            return item.replace('\xa0', '').title()
        except:
            return item

    @staticmethod
    def _getExpansionFromPatch(patch: str) -> str:
        patches = {
            "2": "A Realm Reborn",
            "3": "Heavensward",
            "4": "Stormblood",
            "5": "Shadowbringers",
            "6": "Endwalker"
        }
        return patches[patch.split('.')[0]]


if __name__ == '__main__':
    dungeon_info = DungeonScraper().getDungeon("Amdapor Keep")
    print(json.dumps(dungeon_info, indent=4))
