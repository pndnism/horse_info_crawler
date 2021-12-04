from horse_info_crawler.race.normalizer import UnsupportedFormatError
from pandas.core.frame import DataFrame
import pandas as pd
from horse_info_crawler.race.domain import RaceDetailInfo, RaceInfo, ListingPage
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
from bs4 import BeautifulSoup
import re
from typing import Optional
from horse_info_crawler.components.logger import warning
import urllib
from urllib.parse import urlencode

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"

class RaceInfoListingPageParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html: str) -> ListingPage:
        soup = BeautifulSoup(html, "lxml")

        next_page_url = None
        next_page_element = soup.select_one("div.pager a:contains('次')")
        if next_page_element:
            RACE_LISTING_PAGE_POST_INPUT_DIC["page"] = RACE_LISTING_PAGE_POST_INPUT_DIC.get(
                "page") + 1
            next_page_url = '%s?%s' % (
                NETKEIBA_BASE_URL, urllib.parse.unquote(urlencode(RACE_LISTING_PAGE_POST_INPUT_DIC)))

        race_info_page_urls = [
            i.get("href") for i in soup.find_all(href=re.compile("/race/\d"))]

        return ListingPage(
            next_page_url=next_page_url,
            race_info_page_urls=race_info_page_urls
        )

class RaceInfoParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html) -> RaceInfo:
        soup = BeautifulSoup(html, "lxml")
        return RaceInfo(
            race_url=self._parse_race_url(soup),
            name=self._parse_name(soup),
            race_number=self._parse_race_number(soup),
            course_run_info=self._course_run_info(soup),
            held_info=self._parse_held_info(soup),
            race_detail_info=self._parse_race_details(soup)
        )
    def _parse_race_url(self, soup: BeautifulSoup) -> str:
        if soup.find("a", class_="active", title="R") is None:
            return None
        return NETKEIBA_BASE_URL[:-1] + soup.find("a", class_="active", title="R").get("href")

    def _parse_name(self, soup: BeautifulSoup) -> str:
        if len(soup.find_all("h1")) == 1:
            return None
            #raise UnsupportedFormatError("name not found.")
        return soup.find_all("h1")[1].text

    def _parse_race_number(self, soup: BeautifulSoup) -> str:
        if soup.find("dl", class_="racedata fc") is None:
            return None
        race_number_elem = soup.find("dl", class_="racedata fc").find("dt")
        race_number = re.sub("\n", "", race_number_elem.text)
        return race_number

    def _course_run_info(self, soup: BeautifulSoup) -> str:
        course_run_info_elem = soup.find("diary_snap_cut")
        if course_run_info_elem is None:
            return None
        if course_run_info_elem.find("span") is None:
            return None
        course_run_info = re.sub(u"\xa0", " ", course_run_info_elem.find("span").text)
        return course_run_info

    def _parse_held_info(self, soup: BeautifulSoup) -> str:
        held_info_elem = soup.find("p", class_="smalltxt")
        if held_info_elem is None:
            return None
        held_info = re.sub("\xa0", "", held_info_elem.text)
        held_info = re.sub(" \Z", "", held_info)
        return held_info

    def _parse_race_details(self, soup: BeautifulSoup) -> RaceDetailInfo:
        table = soup.find("table", summary="レース結果")
        if table is None:
            return None
        horse_detail_dict = {}
        for i in table.find_all("th"):
            horse_detail_dict[i.text] = []
        for i in table.find_all('tr'):
            count = 0
            tmp = i.find_all("td")
            for i in tmp:
                horse_detail_dict[list(horse_detail_dict.keys())[count]].append(i)
                count += 1
        race_info_list = [
            "着順","枠番","馬番","馬名","性齢","斤量",
            "騎手","タイム","着差","通過","上り","単勝",
            "人気","馬体重","調教師","馬主","賞金(万円)"
            ]
        for i in race_info_list:
            if i not in horse_detail_dict.keys():
                horse_detail_dict[i] = None
        
        return RaceDetailInfo(
                arrival_orders=horse_detail_dict['着順'],
                box_numbers=horse_detail_dict['枠番'],
                horse_numbers=horse_detail_dict['馬番'],
                horse_info=horse_detail_dict['馬名'],
                horse_ages_and_sexes=horse_detail_dict['性齢'],
                jockey_weights=horse_detail_dict['斤量'],
                jockey_names=horse_detail_dict['騎手'],
                goal_times=horse_detail_dict['タイム'],
                goal_margins=horse_detail_dict['着差'],
                order_transitions=horse_detail_dict['通過'],
                half_times=horse_detail_dict['上り'],
                odds=horse_detail_dict['単勝'],
                popularities=horse_detail_dict['人気'],
                horse_weights=horse_detail_dict['馬体重'],
                trainer_names=horse_detail_dict['調教師'],
                horse_owners=horse_detail_dict['馬主'],
                earn_prizes=horse_detail_dict['賞金(万円)']
        )
