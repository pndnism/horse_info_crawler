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

class HosrseInfoParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html) -> HorseInfo:
        soup = BeautifulSoup(html, "lxml")
        return HorseInfo(
            horse_url=self._parse_horse_url(soup),
            name=self._parse_name(soup),
            birthday=self._parse_birthday(soup),
            trainer_name=self._parse_trainer_name(soup),
            owner_name=self._parse_owner_name(soup),
            producer=self._parse_producer(soup),
            origin_place=self._parse_origin_place(soup),
            mother=self._parse_mother(soup),
            father=self._parse_father(soup),
            mother_of_father=self._parse_mother_of_father(soup),
            father_of_father=self._parse_father_of_father(soup),
            mother_of_mother=self._parse_mother_of_mother(soup),
            father_of_mother=self._parse_father_of_mother(soup)
        )
    def _parse_horse_url(self, soup: BeautifulSoup) -> str:
        if soup.find("a", class_="active", title="R") is None:
            return None
        return NETKEIBA_BASE_URL[:-1] + soup.find("a", class_="active", title="R").get("href")

    def _parse_name(self, soup: BeautifulSoup) -> str:
        if len(soup.find_all("h1")) == 1:
            return None
            #raise UnsupportedFormatError("name not found.")
        return soup.find_all("h1")[1].text

    def _parse_birthday(self, soup: BeautifulSoup) -> Optional[str]:
        if soup.find("dl", class_="racedata fc") is None:
            return None
        race_number_elem = soup.find("dl", class_="racedata fc").find("dt")
        race_number = re.sub("\n", "", race_number_elem.text)
        return race_number

    def _parse_trainer_name(self, soup: BeautifulSoup) -> Optional[str]:
        course_run_info_elem = soup.find("diary_snap_cut")
        if course_run_info_elem is None:
            return None
        if course_run_info_elem.find("span") is None:
            return None
        course_run_info = re.sub(u"\xa0", " ", course_run_info_elem.find("span").text)
        return course_run_info

    def _parse_owner_name(self, soup: BeautifulSoup) -> Optional[str]:
        held_info_elem = soup.find("p", class_="smalltxt")
        if held_info_elem is None:
            return None
        held_info = re.sub("\xa0", "", held_info_elem.text)
        held_info = re.sub(" \Z", "", held_info)
        return held_info

    def _parse_producer(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def _parse_origin_place(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def _parse_mother(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_father(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_mother_of_father(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_father_of_father(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_mother_of_mother(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_father_of_mother(self, soup: BeautifulSoup) -> str:
        pass