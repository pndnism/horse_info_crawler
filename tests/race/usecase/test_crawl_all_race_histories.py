from horse_info_crawler.race.usecases.crawl_all_race_histories import CrawlRaceHistoriesUsecase
from horse_info_crawler.race.repository import RaceInfoRepository
from horse_info_crawler.race.shaper import RaceInfoShaper
from horse_info_crawler.race.domain import ListingPage, RaceInfo, ShapedRaceData
from horse_info_crawler.race.scraper import RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.race.parser import RaceInfoListingPageParser
from unittest import TestCase
from unittest.mock import Mock

import urllib
from urllib.parse import urlencode

from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
from tests.race import helper

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
            race_info_page_urls=[
                "/race/list/0",
                "/race/list/1",
            ]
        )

        race_info_scraper_mock = Mock(spec=RaceInfoScraper)

        test_race = []
        test_race.append(helper.create_race_info(0))
        test_race.append(helper.create_race_info(1))

        race_info_mock_data = {
            "/race/list/0": test_race[0],
            "/race/list/1": test_race[1],
        }

        race_info_shaper_mock = Mock(spec=RaceInfoShaper)
        test_shaped_race_data = []
        test_shaped_race_data.append(helper.create_shaped_race_data(0))
        test_shaped_race_data.append(helper.create_shaped_race_data(1))

        race_info_shaper_mock.shape.side_effect = [test_shaped_race_data[0], test_shaped_race_data[1]]
        
        race_info_repository_mock = Mock(spec=RaceInfoRepository)

        usecase = CrawlRaceHistoriesUsecase(
                race_info_listing_page_scraper=listing_page_requester_mock,
                race_info_scraper= race_info_scraper_mock,
                race_info_shaper=race_info_shaper_mock,
                race_info_repository=race_info_repository_mock)
        usecase.exec()

        race_info_repository_mock.save_shaped_race_info.assert_called_once_with([
            test_shaped_race_data[0],
            test_shaped_race_data[1]
        ])