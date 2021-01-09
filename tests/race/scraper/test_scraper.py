from horse_info_crawler.race.scraper import RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.race.parser import RaceInfoListingPageParser, RaceInfoParser
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

        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="test html", status=200)

        parser_mock = Mock(spec=RaceInfoListingPageParser)
        expected_listing_page = ListingPage(next_page_url=None,
                                            race_info_page_urls=[])

        parser_mock.parse.return_value = expected_listing_page

        listing_page_url = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        listing_page_requester = RaceInfoListingPageScraper(parser_mock)
        result = listing_page_requester.get(listing_page_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         '%s?%s' % (NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)))

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")

        self.assertEqual(result, expected_listing_page)

    @responses.activate
    def test_get_relative_path(self):

        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        test_relative_path = urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)
        responses.add(responses.GET, test_absolute_path,
                      body="test html", status=200)

        parser_mock = Mock(spec=RaceInfoListingPageParser)
        expected_listing_page = ListingPage(next_page_url=None,
                                            race_info_page_urls=[])

        parser_mock.parse.return_value = expected_listing_page

        listing_page_url = "?" + urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)
        listing_page_requester = RaceInfoListingPageScraper(parser_mock)
        result = listing_page_requester.get(listing_page_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         '%s?%s' % (NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)))

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")

        self.assertEqual(result, expected_listing_page)

    @responses.activate
    def test_get_response_error_client(self):
        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="client error", status=404)

        listing_page_url = test_absolute_path
        listing_page_requester = RaceInfoListingPageScraper(
            Mock(spec=RaceInfoListingPageParser))

        with self.assertRaises(HTTPError):
            listing_page_requester.get(listing_page_url)

    @responses.activate
    def test_get_response_error_server(self):
        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="server error", status=500)

        listing_page_url = test_absolute_path
        listing_page_requester = RaceInfoListingPageScraper(
            Mock(spec=RaceInfoListingPageParser))

        with self.assertRaises(HTTPError):
            listing_page_requester.get(listing_page_url)


class TestRaceInfoScraper(TestCase):
    @responses.activate
    def test_get_absolute_path(self):
        responses.add(responses.GET, "https://db.netkeiba.com/race/202005040811/",
                      body="test html", status=200)
        parser_mock = Mock(spec=RaceInfoParser)
        expected_race_info_page = RaceInfo(name=None,
                                           race_number=None,
                                           course_run_info=None,
                                           held_info=None,
                                           race_details=None)
        parser_mock.parse.return_value = expected_race_info_page

        race_info_page_url = "https://db.netkeiba.com/race/202005040811/"
        race_info_page_requester = RaceInfoScraper(parser_mock)

        result = race_info_page_requester.get(race_info_page_url)

        self.assertEqual(len(responses.calls), 1)

        self.assertEqual(responses.calls[0].request.url,
                         "https://db.netkeiba.com/race/202005040811/")

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")
        self.assertEqual(result, expected_race_info_page)

    @responses.activate
    def test_get_relative_path(self):
        responses.add(responses.GET, "https://db.netkeiba.com/race/202005040811/",
                      body="test html", status=200)
        parser_mock = Mock(spec=RaceInfoParser)
        expected_race_info_page = RaceInfo(name=None,
                                           race_number=None,
                                           course_run_info=None,
                                           held_info=None,
                                           race_details=None)
        parser_mock.parse.return_value = expected_race_info_page

        race_info_page_url = "/race/202005040811/"
        race_info_page_requester = RaceInfoScraper(parser_mock)

        result = race_info_page_requester.get(race_info_page_url)

        self.assertEqual(len(responses.calls), 1)

        self.assertEqual(responses.calls[0].request.url,
                         "https://db.netkeiba.com/race/202005040811/")

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")
        self.assertEqual(result, expected_race_info_page)

    @responses.activate
    def test_get_response_error_client(self):
        responses.add(responses.GET, "https://db.netkeiba.com/race/202005040811/",
                      body="client error", status=404)

        race_info_page_url = "https://db.netkeiba.com/race/202005040811/"
        race_info_page_requester = RaceInfoScraper(Mock(spec=RaceInfoParser))

        with self.assertRaises(HTTPError):
            race_info_page_requester.get(race_info_page_url)

    @responses.activate
    def test_get_response_error_server(self):
        responses.add(responses.GET, "https://db.netkeiba.com/race/202005040811/",
                      body="server error", status=500)

        race_info_page_url = "https://db.netkeiba.com/race/202005040811/"
        race_info_page_requester = RaceInfoScraper(Mock(spec=RaceInfoParser))

        with self.assertRaises(HTTPError):
            race_info_page_requester.get(race_info_page_url)
