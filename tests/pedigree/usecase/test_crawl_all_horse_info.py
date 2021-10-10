from unittest.case import TestCase
from unittest.mock import Mock
import urllib
from urllib.parse import urlencode
from horse_info_crawler.pedigree.config import HORSE_LISTING_PAGE_POST_INPUT_DIC
from horse_info_crawler.pedigree.repository import HorseInfoRepository

from horse_info_crawler.pedigree.scraper import HorseInfoListingPageScraper, HorseInfoScraper
from horse_info_crawler.pedigree.domain import ListingPage
from horse_info_crawler.pedigree.shaper import HorseInfoShaper
from horse_info_crawler.pedigree.usecases.crawl_all_horse_info import CrawlHorseInfoUsecase

from tests.pedigree import helper

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"


class TestCrawlHorseInfoUsecase(TestCase):
    def test_no_listing_page_paging(self):
        listing_page_requester_mock = Mock(HorseInfoListingPageScraper)
        LISTING_PAGE_START_URLS = '%s?%s' % (
            NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)))

        listing_page_requester_mock.get.return_value = ListingPage(
            next_page_url=None,
            horse_info_page_urls=[
                "/horse_info/list/0",
                "/horse_info/list/1",
            ]
        )
        horse_info_scraper_mock = Mock(spec=HorseInfoScraper)

        test_horse = []
        test_horse.append(helper.create_horse_info(0))
        test_horse.append(helper.create_horse_info(1))

        horse_info_mock_data = {
            "/horse_info/list/0": test_horse[0],
            "/horse_info/list/1": test_horse[1],
        }

        horse_info_shaper_mock = Mock(spec=HorseInfoShaper)
        test_shaped_horse_data = []
        test_shaped_horse_data.append(helper.create_shaped_horse_data(0))
        test_shaped_horse_data.append(helper.create_shaped_horse_data(1))

        horse_info_shaper_mock.shape.side_effect = [test_shaped_horse_data[0], test_shaped_horse_data[1]]

        horse_info_repository_mock = Mock(spec=HorseInfoRepository)

        usecase = CrawlHorseInfoUsecase(
            horse_info_listing_page_scraper=listing_page_requester_mock,
            horse_info_scraper=horse_info_scraper_mock,
            horse_info_shaper=horse_info_shaper_mock,
            horse_info_repository=horse_info_repository_mock)

        usecase.exec()

        horse_info_repository_mock.save_shaped_horse_info.assert_called_once_with(
            [
               test_shaped_horse_data[0],
               test_shaped_horse_data[1] 
            ]
        )