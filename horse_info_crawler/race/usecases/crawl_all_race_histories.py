from dataclasses import dataclass
from os import name
import urllib
from horse_info_crawler.race.repository import RaceInfoRepository
from horse_info_crawler.race.normalizer import InvalidFormatError, UnsupportedFormatError
from urllib.parse import urlencode
from horse_info_crawler.race.domain import RaceInfo, ShapedRaceData
from typing import Optional, List
from horse_info_crawler.race.shaper import RaceInfoShaper
from horse_info_crawler.race.scraper import DetailPageNotFoundError, NETKEIBA_BASE_URL, RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.components import logger

@dataclass
class CrawlRaceHistoriesUsecase:
    race_info_listing_page_scraper: RaceInfoListingPageScraper
    race_info_scraper: RaceInfoScraper
    race_info_shaper: RaceInfoShaper
    race_info_repository: RaceInfoRepository

    def exec(self, crawl_limit: Optional[int] = None):
        logger.info(f'Start crawl_race_histories. crawl_limit: {crawl_limit}')
        race_histories = self._crawl_race_histories(crawl_limit)

        # race_histories を CSV に変換して ローカルに保存する
        self.race_info_repository.save_shaped_race_info(self._shape_race_infos(race_histories))
        logger.info("End crawl_race_histories.")

    def _crawl_race_histories(self, crawl_limit: Optional[int] = None) -> List[RaceInfo]:
        race_histories = []
        # リスティングページをクロールして物件詳細の URL 一覧を取得する
        listing_page_url = self.race_info_listing_page_scraper.LISTING_PAGE_START_URLS
        while listing_page_url:
            listing_page = self.race_info_listing_page_scraper.get(listing_page_url)
            logger.info(
                f"listing_page_url: {listing_page_url}, race_info_page_urls count: {len(listing_page.race_info_page_urls)}")

            # レース詳細ページにアクセスして、レースのデータを取得する
            for race_info_page_url in listing_page.race_info_page_urls:
                # CSV にアップロードするデータ構造をいれる
                # Errorが発生したら該当PropertyはSkipする
                try:
                    if self._get_race_info(race_info_page_url):
                        race_histories.append(self._get_race_info(race_info_page_url))
                    else:
                        raise DetailPageNotFoundError("table not found.")
                except DetailPageNotFoundError as e:
                    logger.warning(f"Skip getting race:{e}")
                    # TODO: sentryとかエラー監視ツール入れる

                if crawl_limit and len(race_histories) >= crawl_limit:
                    # crawl_limit の件数に達したらクロールを終了する
                    logger.info(f"Finish crawl. race_histories count: {len(race_histories)}")
                    return race_histories

            # next_page_url がある場合は次ページへアクセス
            print(listing_page.next_page_url)
            listing_page_url = listing_page.next_page_url 
        
        logger.info(f"Finish crawl. race_histories count: {len(race_histories)}")
        return race_histories

    def _get_race_info(self, race_info_url: str) -> RaceInfo:
            """
            レースのクロールをして rawデータを返す
            Args:
                race_info_url:
            Returns:
            """
            race_info = self.race_info_scraper.get(race_info_url)
            if race_info.race_detail_info is None:
                return None

            # CSV にアップロードするデータ構造をいれる
            return race_info

    def _shape_race_infos(self, race_info_list: List[RaceInfo]) -> List[ShapedRaceData]:
        shaped_race_info_list = []
        for race_info in race_info_list:
            try:
                # Error が発生したら該当 RaceInfo は Skip する
                shaped_race_info_list.append(self._shape_race_info(race_info))
            except UnsupportedFormatError as e:
                logger.info(f"Skip getting race info:{e}")
                # TODO: エラー検知をsentryとかで実装する
            except InvalidFormatError as e:
                logger.warning(f"Skip getting race info:{e}")
                # TODO: エラー検知をsentryとかで実装する

        return shaped_race_info_list

    def _shape_race_info(self, race_info: RaceInfo) -> ShapedRaceData:
        return self.race_info_shaper.shape(race_info)

    

