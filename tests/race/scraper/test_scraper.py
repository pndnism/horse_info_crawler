from horse_info_crawler.race.scraper import RaceInfoListingPageScraper
from horse_info_crawler.race.parser import RaceInfoListingPageParser
from horse_info_crawler.race.domain import ListingPage, RaceInfo
from unittest import TestCase
from unittest.mock import Mock
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC

import responses
from requests import HTTPError
from urllib.parse import urlencode

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

class TestRaceInfoLisingPageScraper(TestCase):
    @responses.activate
    def test_get_absolute_path(self):

        test_absolute_path = '%s?%s' % (NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path, 
                        body="test html", status=200)

        parser_mock = Mock(spec=RaceInfoListingPageParser)
        expected_listing_page = ListingPage(next_page_post_parameter=None,
                                            next_page_element=None,
                                            race_info_page_urls=[])

        parser_mock.parse.return_value = expected_listing_page

        listing_page_url = '%s?%s' % (NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        listing_page_requester = RaceInfoListingPageScraper(parser_mock)
        result = listing_page_requester.get(listing_page_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         '%s?%s' % (NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)))

        self.assertEqual(parser_mock.parse.call_args.args[0], "test html")

        self.assertEqual(result, expected_listing_page)