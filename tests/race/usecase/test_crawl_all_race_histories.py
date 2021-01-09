from horse_info_crawler.race.domain import ListingPage
from horse_info_crawler.race.scraper import RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.race.parser import RaceInfoListingPageParser
from unittest import TestCase
from unittest.mock import Mock

import urllib
from urllib.parse import urlencode

from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

class TestCrawlRaceHistoriesUsecase(TestCase):
    def test_no_listing_page_paging(self):
        listing_page_requester_mock = Mock(RaceInfoListingPageScraper)
        LISTING_PAGE_START_URLS = '%s?%s' % (
            NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)))
        listing_page_requester_mock.LISTING_PAGE_START_URLS = [
            LISTING_PAGE_START_URLS
        ]

        listing_page_requester_mock.get.return_value = ListingPage(
            next_page_url=None,
            property_detail_page_urls=[
                "/race/list/1",
                "/race/list/2",
            ]
        )

        detail_page_requester_mock = Mock(spec=RaceInfoScraper)

        test_race_1 = helper.create_property(1)
        test_race_2 = helper.create_property(2)