from horse_info_crawler.race.domain import RaceInfo, ListingPage
from horse_info_crawler.race.config import RACE_LISTING_PAGE_POST_INPUT_DIC
from bs4 import BeautifulSoup
import re

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
    def parse(self) -> RaceInfo:
        pass