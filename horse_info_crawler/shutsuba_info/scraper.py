from horse_info_crawler.race.parser import RaceInfoListingPageParser, RaceInfoParser
from horse_info_crawler.race.domain import ListingPage, RaceInfo
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
from dataclasses import dataclass
import urllib
from urllib.parse import urlencode

import requests

from horse_info_crawler.components import logger


class DetailPageNotFoundError(Exception):
    """
    レース詳細ページが見つからない場合のエラー
    """
    pass


NETKEIBA_BASE_URL = "https://race.netkeiba.com/"


@dataclass
class RaceInfoScraper:

    parser: RaceInfoParser

    def get(self, race_info_page_url: str) -> RaceInfo:
        # race_info_parser が相対パスだったら絶対パスに変換数
        race_info_page_absolute_url = urllib.parse.urljoin(
            NETKEIBA_BASE_URL, race_info_page_url)
        logger.info(f"Accessing to {race_info_page_absolute_url}.")
        response = requests.get(race_info_page_absolute_url)
        response.raise_for_status()
        return self.parser.parse(response.content)
