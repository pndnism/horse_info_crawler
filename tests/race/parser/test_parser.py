import os
from types import prepare_class
from unittest import TestCase

from horse_info_crawler.race.parser import RaceInfoListingPageParser, RaceInfoParser
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
import urllib
from urllib.parse import urlencode

from pandas.testing import assert_frame_equal


class TestRaceInfoLisingPageParser(TestCase):
    NETKEIBA_BASE_URL = "https://db.netkeiba.com/"
    def test_parse_normal(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_lising_page.html") as f:
            response_html = f.read()

            parser = RaceInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.next_page_url)
            RACE_LISTING_PAGE_POST_INPUT_DIC["page"] = 2
            self.assertEqual(result.next_page_url,
                             '%s?%s' % (
                                self.NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC))))
            self.assertEqual(len(result.race_info_page_urls), 100)

    def test_parse_normal_last_page(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_last_lising_page.html") as f:
            response_html = f.read()

            parser = RaceInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNone(result.next_page_url)


class TestRaceInfoParser(TestCase):
    def test_parse_normal(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_race_info.html") as f:
            response_html = f.read()

            parser = RaceInfoParser()
            result = parser.parse(response_html)

            self.assertIsNotNone(result)
            self.assertEqual(result.race_url, "https://db.netkeiba.com/race/202035111401/")
            self.assertEqual(result.name, "C2十三組")
            self.assertEqual(result.race_number, "1 R")
            self.assertEqual(result.course_run_info,
                             "ダ左1200m / 天候 : 曇 / ダート : 稍重 / 発走 : 11:50")
            self.assertEqual(result.held_info, "2020年11月14日 11回盛岡1日目")
            #self.assertEqual(result.race_detail_info, pd.read_pickle(
            #    f"{os.path.dirname(__file__)}/../normalizer/data/test_race_info_dict.pickle"))
