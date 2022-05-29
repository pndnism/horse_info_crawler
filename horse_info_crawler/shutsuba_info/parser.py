from horse_info_crawler.components import logger
from horse_info_crawler.shutsuba_info.normalizer import UnsupportedFormatError
from pandas.core.frame import DataFrame
import pandas as pd
from horse_info_crawler.shutsuba_info.domain import RaceDetailInfo, RaceInfo
from horse_info_crawler.shutsuba_info.config import SHUTUBA_RACE_INFO
from bs4 import BeautifulSoup
import re
from typing import List, Optional
from horse_info_crawler.components.logger import warning
import urllib
from urllib.parse import urlencode

NETKEIBA_BASE_URL = "https://db.netkeiba.com/"


class RaceInfoParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """

    def parse(self, html) -> RaceInfo:
        soup = BeautifulSoup(html, "lxml")
        return RaceInfo(
            race_url=self._parse_race_url(soup),
            name=self._parse_name(soup),
            race_number=SHUTUBA_RACE_INFO["race_num"],
            course_run_info=self._course_run_info(soup),
            held_date=self._parse_held_info(soup)[0],
            held_info=self._parse_held_info(soup)[1],
            race_detail_info=self._parse_race_details(soup),
        )

    def _parse_race_url(self, soup: BeautifulSoup) -> str:
        if soup.find("meta", attrs={"property": "og:url"}) is None:
            return None
        return soup.find("meta", attrs={"property": "og:url"}).get("content")

    def _parse_name(self, soup: BeautifulSoup) -> str:
        if not soup.find("div", class_="RaceName"):
            return None
            #raise UnsupportedFormatError("name not found.")
        race_name = soup.find("div", class_="RaceName").text
        return re.sub("\n", "", race_name)

    def _parse_race_number(self, soup: BeautifulSoup) -> str:
        if soup.find("dl", class_="racedata fc") is None:
            return None
        race_number_elem = soup.find("dl", class_="racedata fc").find("dt")
        race_number = re.sub("\n", "", race_number_elem.text)
        return race_number

    def _course_run_info(self, soup: BeautifulSoup) -> str:
        course_run_info_elem = soup.find("div", class_="RaceData01")
        if course_run_info_elem is None:
            return None
        course_run_info = re.sub(r"\n", " ", course_run_info_elem.text)
        return course_run_info

    def _parse_held_info(self, soup: BeautifulSoup) -> str:
        title_ = soup.title.text
        held_date = re.search(r"\d{4}年\d+月\d+日", title_).group()
        held_info_elem = soup.find("div", class_="RaceData02")
        if held_info_elem is None:
            return None
        held_info = re.sub("\xa0", "", held_info_elem.text)
        held_info = re.sub(r" \n", "", held_info)
        return held_date, held_info

    def _parse_race_details(self, soup: BeautifulSoup) -> RaceDetailInfo:
        table = soup.find_all("table")
        if table is None:
            return None
        df = pd.read_html(str(table))[0]
        df.columns = df.columns.get_level_values(0)
        horse_detail_dict = df.to_dict('list')
        horse_list = table[0].find_all("span", class_="HorseName")

        horse_ids = [re.search(r"\d{10}", horse.find("a").get("href")).group()
                     for horse in horse_list if horse.find("a")]

        return RaceDetailInfo(
            box_numbers=horse_detail_dict['枠'],
            horse_numbers=horse_detail_dict['馬番'],
            horse_info=horse_detail_dict['馬名'],
            horse_ages_and_sexes=horse_detail_dict['性齢'],
            jockey_weights=horse_detail_dict['斤量'],
            jockey_names=horse_detail_dict['騎手'],
            popularities=horse_detail_dict['人気'],
            horse_weights=horse_detail_dict['馬体重(増減)'],
            trainer_names=horse_detail_dict['厩舎'],
            horse_ids=horse_ids)
