from horse_info_crawler.race.domain import ListingPage
from dataclasses import dataclass

import requests

from horse_info_crawler.components import logger

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

@dataclass
class RaceInfoListingPageScraper:
    LISTING_PAGE_START_URLS = [
        "https://db.netkeiba.com/?pid=race_list&word=&track%5B%5D=1&track%5B%5D=2&start_year=none&start_mon=none&end_year=none&end_mon=none&kyori_min=&kyori_max=&sort=date&list=100",
    ]