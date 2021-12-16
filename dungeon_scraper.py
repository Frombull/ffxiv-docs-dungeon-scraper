import json
import logging as log
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

log.basicConfig(level=log.INFO,
                format='[%(levelname)s] (%(asctime)s) - %(message)s',
                datefmt='%H:%M:%S')


@dataclass()
class Dungeons:
    name: str = 'N/A'
    type: str = 'N/A'
    level: str = 'N/A'
    ilevel: str = 'N/A'
    expansion: str = 'N/A'
    patch: str = 'N/A'
    difficulty: str = 'N/A'
    party_size: str = 'N/A'
    url: str = 'N/A'

    @classmethod
    def get(cls, dg_name: str) -> dict:
        dg_name_filtered = cls._formatNameToUrl(dg_name)
        URL = f"https://ffxiv.consolegameswiki.com/mediawiki/index.php?search={dg_name_filtered}"

        log.info(f'Getting dungeon: {dg_name}, from url: {URL}')

        r = requests.get(url=URL, headers=HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        if r.status_code == 404:
            log.error(f'HTTP {r.status_code}, Could not find dungeon: {dg_name}')
            raise NameError(f'HTTP {r.status_code}, Could not find dungeon: {dg_name}')

        # Check if the page is a dungeon page
        try:
            infobox = soup.find('div', class_='infobox-n duty')
            cls.name = infobox.find('p', class_='heading').text.strip()
        except AttributeError:
            log.error(f'Could not find dungeon: {dg_name}')
            return None
            # raise NameError(f'Could not find dungeon: {dg_name}')

        wrappers = infobox.find('div', class_='wrapper').find_all('dl')

        wrapper_final = []
        for wrapper in wrappers:
            for i, item in enumerate(wrapper):
                if len(str(item)) > 4:
                    wrapper_final.append(str(item).strip().lower())

        for i, item in enumerate(wrapper_final):
            next_index = i + 1
            if next_index >= len(wrapper_final):
                break
            next_item = wrapper_final[next_index]

            if '>difficulty<' in item:
                cls.difficulty = cls._filterTags(next_item)
            elif '>level<' in item:
                cls.level = cls._filterTags(next_item)
            elif '>ilevel<' in item:
                cls.ilevel = cls._filterTags(next_item)
            elif '>patch<' in item:
                cls.patch = next_item.split('</a>')[0].split('">')[1]
                cls.expansion = cls._getExpansionFromPatch(cls.patch)
            elif '>party size<' in item:
                if 'Alliance' in next_item:
                    cls.party_size = 'Alliance'
                else:
                    cls.party_size = cls._filterTags(next_item)
                    cls.party_size = (cls.party_size.split('Party')[0]).title()

        main_page = soup.find('div', class_='mw-parser-output')
        for p in main_page.find_all('p'):
            if 'href="/wiki/Dungeon"' in str(p):
                cls.type = 'Dungeon'
                break
            elif 'href="/wiki/Trial"' in str(p):
                cls.type = 'Trial'
                break
            elif 'href="/wiki/Raid"' in str(p):
                cls.type = 'Raid'
                break

        return {
            "name": cls.name,
            "type": cls.type,
            "level": cls.level,
            "ilevel": cls.ilevel,
            "expansion": cls.expansion,
            "patch": cls.patch,
            "difficulty": cls.difficulty,
            "party_size": cls.party_size,
            "url": URL
        }

    @staticmethod
    def _formatNameToUrl(dg_name: str) -> str:
        return dg_name.strip().title().replace(' ', '_').replace("'", '%27')

    @staticmethod
    def _filterTags(item: str) -> str:
        try:
            return item[1:].split('<')[0].split('>')[1].replace('\xa0', '').title()
        except IndexError:
            return item.replace('\xa0', '').title()

    @staticmethod
    def _getExpansionFromPatch(patch: str) -> str:
        patch_first_num = str(patch.split('.')[0])
        return {
            "2": "A Realm Reborn",
            "3": "Heavensward",
            "4": "Stormblood",
            "5": "Shadowbringers",
            "6": "Endwalker"
        }.get(patch_first_num, 'N/A')

    def __str__(self):
        return json.dumps(vars(self), indent=2)
