from typing import Optional
from horse_info_crawler.pedigree.domain import HorseInfo, ListingPage
from bs4 import BeautifulSoup
from horse_info_crawler.pedigree.config import HORSE_LISTING_PAGE_POST_INPUT_DIC
import urllib
from urllib.parse import urlencode
import re


NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

class HorseInfoListingPageParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html: str) -> ListingPage:
        soup = BeautifulSoup(html, "html.parser")


        next_page_url = None
        next_page_element = soup.select_one("div.pager a:contains('次')")
        if next_page_element:
            HORSE_LISTING_PAGE_POST_INPUT_DIC["page"] = HORSE_LISTING_PAGE_POST_INPUT_DIC.get(
                "page") + 1
            next_page_url = '%s?%s' % (
                NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(HORSE_LISTING_PAGE_POST_INPUT_DIC)))

        horse_info_page_urls = [
            i.get("href") for i in soup.find_all(href=re.compile("/horse/\d"))]

        return ListingPage(
            next_page_url=next_page_url,
            horse_info_page_urls=horse_info_page_urls
        )

class HorseInfoParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html) -> HorseInfo:
        soup = BeautifulSoup(html, "lxml")
        profile_table = soup.find_all("table", class_="db_prof_table no_OwnerUnit")[0]
        profile_dic = {}
        for i,j in zip(profile_table.find_all("th"), profile_table.find_all("td")):
            profile_dic[i.text] = j.text

        blood_table = soup.find_all("dd", class_="DB_ProfHead_dd_01")[0]
        return HorseInfo(
            horse_url=self._parse_horse_url(soup),
            name=self._parse_name(soup),
            birthday=self._parse_birthday(profile_dic),
            trainer_name=self._parse_trainer_name(profile_dic),
            owner_name=self._parse_owner_name(profile_dic),
            producer=self._parse_producer(profile_dic),
            origin_place=self._parse_origin_place(profile_dic),
            mother=self._parse_mother(blood_table),
            father=self._parse_father(blood_table),
            mother_of_father=self._parse_mother_of_father(blood_table),
            father_of_father=self._parse_father_of_father(blood_table),
            mother_of_mother=self._parse_mother_of_mother(blood_table),
            father_of_mother=self._parse_father_of_mother(blood_table)
        )
    def _parse_horse_url(self, soup: BeautifulSoup) -> str:
        if soup.find("meta", property="og:url") is None:
            return None
        return soup.find("meta", property="og:url").get("content")

    def _parse_name(self, soup: BeautifulSoup) -> str:
        if len(soup.find_all("h1")) == 1:
            return None
            #raise UnsupportedFormatError("name not found.")
        name = soup.find_all("h1")[1].text
        return ''.join(name.split())

    def _parse_birthday(self, profile_dic: dict) -> Optional[str]:
        return profile_dic["生年月日"]

    def _parse_trainer_name(self, profile_dic: dict) -> Optional[str]:
        return profile_dic["調教師"]

    def _parse_owner_name(self, profile_dic: dict) -> Optional[str]:
        return profile_dic["馬主"]

    def _parse_producer(self, profile_dic: dict) -> Optional[str]:
        return profile_dic["生産者"]

    def _parse_origin_place(self, profile_dic: dict) -> Optional[str]:
        return profile_dic["産地"]

    def _parse_mother(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[3].text

    def _parse_father(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[0].text

    def _parse_mother_of_father(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[2].text

    def _parse_father_of_father(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[1].text

    def _parse_mother_of_mother(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[5].text

    def _parse_father_of_mother(self, blood_table: BeautifulSoup) -> str:
        return blood_table.find_all("a")[4].text