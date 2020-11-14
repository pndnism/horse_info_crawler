import os
from types import prepare_class
from unittest import TestCase

from horse_info_crawler.race.parser import RaceInfoListingPageParser, RaceInfo
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC

class TestRaceInfoLisingPageParser(TestCase):
    def test_parse_normal(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_lising_page.html") as f:
            response_html = f.read()

            parser = RaceInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.next_page_element)
            RACE_LISTING_PAGE_POST_INPUT_DIC["page"]=2
            self.assertEqual(result.next_page_post_parameter, RACE_LISTING_PAGE_POST_INPUT_DIC)
            self.assertEqual(len(result.race_info_page_urls), 100)

    def test_parse_normal_last_page(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_last_lising_page.html") as f:
            response_html = f.read()

            parser = RaceInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNone(result.next_page_element)    

class TestRaceInfoParser(TestCase):
    def test_parse_normal(self):
        pass
