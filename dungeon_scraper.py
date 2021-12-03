import json
import logging as log

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

        # TODO: Finish this stuff lmao
        # wrapper_1 = list(wrappers.find_all('dl')[0])
        wrapper_2 = list(wrappers.find_all('dl')[1])
        # print(wrapper_1[0])
        # for i in :
        # print(i.text)
        # print('-'*30)
        # dg_level = .find('Level')

        # party_size = infobox.find('', class_='').text.strip()

        # print(dg_level)

        return json.dumps({
            "name": dg_name,
            "type": url,
            "expansion": url,
            "level": url,
            "partySize": url,
        })

    @staticmethod
    def _filterDgName(dg_name: str) -> str:
        log.info('Filtering dungeon name')
        return dg_name.strip().replace(' ', '_')


if __name__ == '__main__':
    DungeonScraper().getDungeon('Dun_Scaith')
