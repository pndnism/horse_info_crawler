from pandas.core.frame import DataFrame
import pandas as pd
from horse_info_crawler.race.domain import RaceInfo, ListingPage
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
from bs4 import BeautifulSoup
import re
from typing import Optional
from horse_info_crawler.components.logger import warning

class RaceInfoListingPageParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """
    def parse(self, html:str) -> ListingPage:
        soup = BeautifulSoup(html, "html.parser")

        next_page_post_parameter=None
        next_page_element = soup.select_one("div.pager a:contains('次')")
        if next_page_element:
            RACE_LISTING_PAGE_POST_INPUT_DIC["page"] = RACE_LISTING_PAGE_POST_INPUT_DIC.get("page") + 1
            next_page_post_parameter = RACE_LISTING_PAGE_POST_INPUT_DIC
        
        race_info_page_urls = [i.get("href") for i in soup.find_all(href=re.compile("/race/\d"))]

        return ListingPage(
            next_page_element=next_page_element,
            next_page_post_parameter=next_page_post_parameter,
            race_info_page_urls=race_info_page_urls
        )


class RaceInfoParser:
    """
    取得したHTMLをパースして構造化したデータに変換する
    """
    def parse(self, html) -> RaceInfo:
        soup = BeautifulSoup(html, "html.parser")

        return RaceInfo(
            name=self._parse_name(soup),
            race_number=self._parse_race_number(soup),
            course_run_info=self._course_run_info(soup),
            held_info=self._parse_held_info(soup),
            race_details=self._parse_race_details(soup)
        )

    def _parse_name(self, soup: BeautifulSoup) -> str:
        return soup.find_all("h1")[1].text

    def _parse_race_number(self, soup: BeautifulSoup) -> str:
        pass

    def _course_run_info(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_held_info(self, soup: BeautifulSoup) -> str:
        pass

    def _parse_race_details(self, soup: BeautifulSoup) -> DataFrame:
        table = soup.find("table", summary="レース結果")
        rows = table.find_all("tr")
        columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]
        df = pd.DataFrame(columns=columns)
        # 全行のうちのある行成分について
        for i in range(len(rows)):
            # 全ての<td>タグ（セルデータ）を取得しtdsに格納、リスト化
            tds = rows[i].find_all('td')
            # tdsのデータ数がカラム数に一致しない場合（ブランク）などは排除し、
            if len(tds) == len(columns):
                # （ある行成分の）全セルデータをテキスト成分としてvaluesに格納、リスト化
                values = [ td.text.replace('\n', '').replace('\xa0', ' ') for td in tds ]
                # valuesをpd.seriesデータに変換、データフレームに結合
                df = df.append(pd.Series(values, index=columns), ignore_index= True)
        return df