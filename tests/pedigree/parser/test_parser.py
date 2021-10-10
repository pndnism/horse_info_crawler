from horse_info_crawler.pedigree.parser import HorseInfoListingPageParser, HorseInfoParser
from unittest.case import TestCase
from horse_info_crawler.pedigree.config import HORSE_LISTING_PAGE_POST_INPUT_DIC
import urllib
from urllib.parse import urlencode
import os



class TestHorseInfoLisingPageParser(TestCase):
    NETKEIBA_BASE_URL = "https://db.netkeiba.com/"
    def test_parse_normal(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_listing_page.html") as f:
            response_html = f.read()

            parser = HorseInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.next_page_url)
            HORSE_LISTING_PAGE_POST_INPUT_DIC["page"] = 2
            self.assertEqual(result.next_page_url,
                             '%s?%s' % (
                                self.NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC))))
            self.assertEqual(len(result.horse_info_page_urls), 20)

    def test_parse_normal_last_page(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_last_listing_page.html") as f:
            response_html = f.read()

            parser = HorseInfoListingPageParser()
            result = parser.parse(response_html)
            self.assertIsNotNone(result)
            self.assertIsNone(result.next_page_url)


class TestHorseInfoParser(TestCase):
    def test_parse_normal(self):
        with open(f"{os.path.dirname(__file__)}/data/test_parse_normal_horse_info.html") as f:
            response_html = f.read()

            parser = HorseInfoParser()
            result = parser.parse(response_html, "https://db.netkeiba.com/horse/2014102226/")

            self.assertIsNotNone(result)
            self.assertEqual(result.horse_url, "https://db.netkeiba.com/horse/2014102226/")
            self.assertEqual(result.name, "デザートストーム")
            self.assertEqual(result.birthday, "2014年4月11日")
            self.assertEqual(result.trainer_name, "西浦勝一 (栗東)")
            self.assertEqual(result.owner_name, "ゴドルフィン")
            self.assertEqual(result.producer, "ダーレー・ジャパン・ファーム")
            self.assertEqual(result.origin_place, "日高町")
            self.assertEqual(result.mother, "レディオブパーシャ")
            self.assertEqual(result.father, "ストーミングホーム")
            self.assertEqual(result.mother_of_father, "Try to Catch Me")
            self.assertEqual(result.father_of_father, "Machiavellian")
            self.assertEqual(result.mother_of_mother, "ビールジャント")
            self.assertEqual(result.father_of_mother, "Shamardal")