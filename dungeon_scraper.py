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

        # TODO: Deixar essa parada dos wrapper_x automatica, pq as vezes tem uns 4 e as vezes uns 2 ¬¬
        wrappers = infobox.find('div', class_='wrapper')

        wrapper_1_raw = list(wrappers.find_all('dl')[0])
        wrapper_2_raw = list(wrappers.find_all('dl')[1])
        wrapper_1 = list(filter(lambda x: len(str(x)) > 4, wrapper_1_raw))
        wrapper_2 = list(filter(lambda x: len(str(x)) > 4, wrapper_2_raw))

        # TODO: Deixar também "automatico", pq as vezes tem uns 4
        for i, item in enumerate(wrapper_1):
            # print(f'{i}, {item}')
            if '>difficulty<' in str(item).strip().lower():
                next_item = str(wrapper_1[i + 1])
                dg_difficulty = self._filterTags(next_item)
            elif '>level<' in str(item).strip().lower():
                next_item = str(wrapper_1[i + 1])
                dg_level = self._filterTags(next_item)
            elif '>ilevel<' in str(item).strip().lower():
                next_item = str(wrapper_1[i + 1])
                dg_ilevel = self._filterTags(next_item)

        for i, item in enumerate(wrapper_2):
            if '>patch<' in str(item).strip().lower():
                next_item = wrapper_2[i + 1]
                dg_patch = self._filterTags(str(next_item.text))
                dg_expansion = self._getExpansionFromPatch(dg_patch)
            elif '>party size<' in str(item).strip().lower():
                next_item = wrapper_2[i + 1]
                if 'Alliance' in next_item:
                    dg_party_size = 'Alliance'
                else:
                    dg_party_size = self._filterTags(str(next_item.text))
                    dg_party_size = dg_party_size.split('Party')[0] + 'Party'



        main_page = soup.find('div', class_='mw-parser-output')
        p_list = main_page.find_all('p')
        for p in p_list:
            if 'href="/wiki/Dungeon"' in str(p):
                dg_type = 'Dungeon'
            elif 'href="/wiki/Trial"' in str(p):
                dg_type = 'Trial'
            elif 'href="/wiki/Raid"' in str(p):
                dg_type = 'Raid'


        # TODO: Deixar tudo por padrão como 'None' ou sei lá
        return {
            "name": dg_name,
            "type": dg_type,
            "expansion": dg_expansion,
            "patch": dg_patch,
            "level": dg_level,
            "ilevel": dg_ilevel,
            "dificulty": dg_difficulty,
            "partySize": dg_party_size,
            "url": URL
        }

    @staticmethod
    def _filterDgName(dg_name: str) -> str:
        log.info(f'Filtering dungeon name: {dg_name}')
        return dg_name.strip().replace(' ', '_').replace("'", '%27').title()

    # TODO: Se pa é melhor remover essa porra toda aqui e pegar o conteudo do objeto bs4 (.text)
    @staticmethod
    def _filterTags(item: str) -> str:
        # log.info('Filtering item tags')
        try:
            return item[1:].split('<')[0].split('>')[1].replace('\xa0', '')
        except IndexError:
            return item.replace('\xa0', '')
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
    dungeon_info = DungeonScraper().getDungeon("AmDapor_KEEp")
    print(json.dumps(dungeon_info, indent=4))
