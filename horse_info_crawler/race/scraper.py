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

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"


@dataclass
class RaceInfoListingPageScraper:
    LISTING_PAGE_START_URLS = '%s?%s' % (
        NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
    parser: RaceInfoListingPageParser

    def get(self, listing_page_url: str) -> ListingPage:
        # listing_page_url が相対パスだったら絶対パスに変換する
        listing_page_absolute_url = urllib.parse.urljoin(
            NETKEIBA_BASE_URL, listing_page_url)
        logger.info(f"Accessing to {listing_page_absolute_url}.")
        response = requests.get(listing_page_absolute_url)
        response.raise_for_status()
        return self.parser.parse(response.content)


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
