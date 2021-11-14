from horse_info_crawler.components import logger
from horse_info_crawler.race.normalizer import UnsupportedFormatError
from pandas.core.frame import DataFrame
import pandas as pd
from horse_info_crawler.race.domain import RaceDetailInfo, RaceInfo, ListingPage, PayResult
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
        soup = BeautifulSoup(html, "html.parser")
        
        next_page_url = None
        next_page_element = soup.select_one("div.pager a:contains('次')")
        
        # ページによってパーサーを変えないと正常にパースできないパースがあるので、その対応
        if not next_page_element:
            soup = BeautifulSoup(html, "lxml")
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
            race_detail_info=self._parse_race_details(soup),
            pay_result=self._parse_pay_result(soup)
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

    def _parse_pay_result(self, soup: BeautifulSoup):
        tables = soup.find_all("table", summary="払い戻し")
        if len(tables) == 0:
            logger.warning("no payresult data.")
            return None
        pay_result_dict = {}
        for table in tables:
            count = 0
            for i in table.find_all("th"):
                pay_result_dict[i.text] = [i.get_text(',').split(',') for i in table.find_all("tr")[count].find_all("td")]
                count += 1
        if "単勝" not in pay_result_dict.keys() or len(pay_result_dict["単勝"][0]) != 1:
            pay_result_dict["単勝"] = [[None],[None]]
        if "複勝" not in pay_result_dict.keys() or len(pay_result_dict["複勝"][0]) != 3:
            pay_result_dict["複勝"] = [[None,None,None],[None,None,None],[None,None,None]]
        if "馬連" not in pay_result_dict.keys():
            pay_result_dict["馬連"] = [[None,None,None],[None,None,None],[None,None,None]]
        if "ワイド" not in pay_result_dict.keys() or len(pay_result_dict["ワイド"][0]) != 3:
            pay_result_dict["ワイド"] = [[None,None,None],[None,None,None],[None,None,None]]
        if "馬単" not in pay_result_dict.keys():
            pay_result_dict["馬単"] = [[None,None,None],[None,None,None],[None,None,None]]
        if "三連単" not in pay_result_dict.keys():
            pay_result_dict["三連単"] = [[None,None,None],[None,None,None],[None,None,None]]
        if "三連複" not in pay_result_dict.keys():
            pay_result_dict["三連複"] = [[None,None,None],[None,None,None],[None,None,None]]

        return PayResult(
            tansho=pay_result_dict["単勝"],
            fukusho=pay_result_dict["複勝"],
            umaren=pay_result_dict["馬連"],
            wide=pay_result_dict["ワイド"],
            umatan=pay_result_dict["馬単"],
            sanrentan=pay_result_dict["三連単"],
            sanrenpuku=pay_result_dict["三連複"]
        )
