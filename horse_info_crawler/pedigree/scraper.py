from horse_info_crawler.pedigree.parser import HorseInfoListingPageParser, HorseInfoParser
from horse_info_crawler.pedigree.domain import ListingPage, HorseInfo
from horse_info_crawler.pedigree.config import HORSE_LISTING_PAGE_POST_INPUT_DIC
from dataclasses import dataclass
import urllib
from urllib.parse import urlencode
import subprocess
import socks,socket

import requests

from horse_info_crawler.components import logger

class DetailPageNotFoundError(Exception):
    """
    レース詳細ページが見つからない場合のエラー
    """
    pass

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

@dataclass
class HorseInfoListingPageScraper:
    # TODO: mechanical_soupとかrobobrowserとか使ってみる
    # sessionをここで保持する必要がある
    LISTING_PAGE_START_URLS = '%s?%s' % (
        NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)))
    parser: HorseInfoListingPageParser

    def get(self, listing_page_url: str) -> ListingPage:
        # listing_page_url が相対パスだったら絶対パスに変換する
        listing_page_absolute_url = urllib.parse.urljoin(
            NETKEIBA_BASE_URL, listing_page_url)
        logger.info(f"Accessing to {listing_page_absolute_url}.")
        response = requests.get(listing_page_absolute_url)
        response.raise_for_status()
        return self.parser.parse(response.content)


@dataclass
class HorseInfoScraper:

    parser: HorseInfoParser

    def get(self, horse_info_page_url: str) -> HorseInfo:
        #args = ['sudo', 'service', 'tor','restart']
        #subprocess.call(args)
        #socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        #socket.socket = socks.socksocket
        #proxies = {
        #'http':'socks5://127.0.0.1:9050',
        #'https':'socks5://127.0.0.1:9050'
        #}
        # horse_info_parser が相対パスだったら絶対パスに変換数
        horse_info_page_absolute_url = urllib.parse.urljoin(
            NETKEIBA_BASE_URL, horse_info_page_url)
        logger.info(f"Accessing to {horse_info_page_absolute_url}.")
        response = requests.get(horse_info_page_absolute_url)
        #print(response)
        response.raise_for_status()
        return self.parser.parse(response.content, horse_info_page_absolute_url)
