from horse_info_crawler.pedigree.scraper import HorseInfoListingPageScraper, HorseInfoScraper
from horse_info_crawler.pedigree.parser import HorseInfoListingPageParser, HorseInfoParser
from horse_info_crawler.pedigree.domain import ListingPage, HorseInfo
from unittest import TestCase
from unittest.mock import Mock
from horse_info_crawler.pedigree.config import HORSE_LISTING_PAGE_POST_INPUT_DIC

import responses
from requests import HTTPError
from urllib.parse import urlencode

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"


class TestHorseInfoLisingPageScraper(TestCase):
    @responses.activate
    def test_get_absolute_path(self):

        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="test html", status=200)

        parser_mock = Mock(spec=HorseInfoListingPageParser)
        expected_listing_page = ListingPage(next_page_url=None,
                                            horse_info_page_urls=[])

        parser_mock.parse.return_value = expected_listing_page

        listing_page_url = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))
        listing_page_requester = HorseInfoListingPageScraper(parser_mock)
        result = listing_page_requester.get(listing_page_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         '%s?%s' % (NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)))

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")

        self.assertEqual(result, expected_listing_page)

    @responses.activate
    def test_get_relative_path(self):

        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))
        test_relative_path = urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)
        responses.add(responses.GET, test_absolute_path,
                      body="test html", status=200)

        parser_mock = Mock(spec=HorseInfoListingPageParser)
        expected_listing_page = ListingPage(next_page_url=None,
                                            horse_info_page_urls=[])

        parser_mock.parse.return_value = expected_listing_page

        listing_page_url = "?" + urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)
        listing_page_requester = HorseInfoListingPageScraper(parser_mock)
        result = listing_page_requester.get(listing_page_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         '%s?%s' % (NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)))

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")

        self.assertEqual(result, expected_listing_page)

    @responses.activate
    def test_get_response_error_client(self):
        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="client error", status=404)

        listing_page_url = test_absolute_path
        listing_page_requester = HorseInfoListingPageScraper(
            Mock(spec=HorseInfoListingPageParser))

        with self.assertRaises(HTTPError):
            listing_page_requester.get(listing_page_url)

    @responses.activate
    def test_get_response_error_server(self):
        test_absolute_path = '%s?%s' % (
            NETKEIBA_BASE_URL, urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))
        responses.add(responses.GET, test_absolute_path,
                      body="server error", status=500)

        listing_page_url = test_absolute_path
        listing_page_requester = HorseInfoListingPageScraper(
            Mock(spec=HorseInfoListingPageParser))

        with self.assertRaises(HTTPError):
            listing_page_requester.get(listing_page_url)


class TestHorseInfoScraper(TestCase):
    @responses.activate
    def test_get_absolute_path(self):
        responses.add(responses.GET, "https://db.netkeiba.com/horse/2014102226/",
                      body="test html", status=200)
        parser_mock = Mock(spec=HorseInfoParser)
        expected_horse_info_page = HorseInfo(horse_url=None,
                                            name=None,
                                            birthday=None,
                                            trainer_name=None,
                                            owner_name=None,
                                            producer=None,
                                            origin_place=None,
                                            mother=None,
                                            father=None,
                                            mother_of_father=None,
                                            father_of_father=None,
                                            mother_of_mother=None,
                                            father_of_mother=None)
        parser_mock.parse.return_value = expected_horse_info_page

        horse_info_page_url = "https://db.netkeiba.com/horse/2014102226/"
        horse_info_page_requester = HorseInfoScraper(parser_mock)

        result = horse_info_page_requester.get(horse_info_page_url)

        self.assertEqual(len(responses.calls), 1)

        self.assertEqual(responses.calls[0].request.url,
                         "https://db.netkeiba.com/horse/2014102226/")

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")
        self.assertEqual(result, expected_horse_info_page)

    @responses.activate
    def test_get_relative_path(self):
        responses.add(responses.GET, "https://db.netkeiba.com/horse/2014102226/",
                      body="test html", status=200)
        parser_mock = Mock(spec=HorseInfoParser)
        expected_horse_info_page = HorseInfo(horse_url=None,
                                            name=None,
                                            birthday=None,
                                            trainer_name=None,
                                            owner_name=None,
                                            producer=None,
                                            origin_place=None,
                                            mother=None,
                                            father=None,
                                            mother_of_father=None,
                                            father_of_father=None,
                                            mother_of_mother=None,
                                            father_of_mother=None)
        parser_mock.parse.return_value = expected_horse_info_page

        horse_info_page_url = "/horse/2014102226/"
        horse_info_page_requester = HorseInfoScraper(parser_mock)

        result = horse_info_page_requester.get(horse_info_page_url)

        self.assertEqual(len(responses.calls), 1)

        self.assertEqual(responses.calls[0].request.url,
                         "https://db.netkeiba.com/horse/2014102226/")

        self.assertEqual(parser_mock.parse.call_args.args[0], b"test html")
        self.assertEqual(result, expected_horse_info_page)

    @responses.activate
    def test_get_response_error_client(self):
        responses.add(responses.GET, "https://db.netkeiba.com/horse/2014102226/",
                      body="client error", status=404)

        horse_info_page_url = "https://db.netkeiba.com/horse/2014102226/"
        horse_info_page_requester = HorseInfoScraper(Mock(spec=HorseInfoParser))

        with self.assertRaises(HTTPError):
            horse_info_page_requester.get(horse_info_page_url)

    @responses.activate
    def test_get_response_error_server(self):
        responses.add(responses.GET, "https://db.netkeiba.com/horse/2014102226/",
                      body="server error", status=500)

        horse_info_page_url = "https://db.netkeiba.com/horse/2014102226/"
        horse_info_page_requester = HorseInfoScraper(Mock(spec=HorseInfoParser))

        with self.assertRaises(HTTPError):
            horse_info_page_requester.get(horse_info_page_url)
