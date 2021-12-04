from dataclasses import dataclass
from os import name
import urllib
from horse_info_crawler.race.repository import RaceInfoRepository
from horse_info_crawler.race.normalizer import InvalidFormatError, UnsupportedFormatError
from urllib.parse import urlencode
import glob
import pandas as pd
from horse_info_crawler.race.domain import RaceInfo, ShapedRaceData
from typing import Optional, List
from horse_info_crawler.race.shaper import RaceInfoShaper
from horse_info_crawler.race.scraper import DetailPageNotFoundError, NETKEIBA_BASE_URL, RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.components import logger
import gc

@dataclass
class CrawlRaceHistoriesUsecase:
    race_info_listing_page_scraper: RaceInfoListingPageScraper
    race_info_scraper: RaceInfoScraper
    race_info_shaper: RaceInfoShaper
    race_info_repository: RaceInfoRepository

    def exec(self, crawl_limit: Optional[int] = None):

        # while 
        # logger.info(f'Start crawl_race_histories. crawl_limit: {crawl_limit}')
        # race_histories = self._crawl_race_histories(crawl_limit)

        # # race_histories を CSV に変換して ローカルに保存する
        # self.race_info_repository.save_shaped_race_info(self._shape_race_infos(race_histories))
        # logger.info("End crawl_race_histories.")
        listing_page_url = self.race_info_listing_page_scraper.LISTING_PAGE_START_URLS
        crawled_urls = self._check_crawled_urls()
        while listing_page_url:
            race_histories, next_listing_url = self._crawl_race_histories(crawl_limit, listing_page_url, crawled_urls)
            self.race_info_repository.save_shaped_race_info(self._shape_race_infos(race_histories))
            listing_page_url = next_listing_url
            del race_histories
            gc.collect()

    def _prepare_to_check_saved_urls():
        pass
    
    def _crawl_race_histories(self, crawl_limit: Optional[int] = None, listing_page_url: str = None, crawled_urls: List[str] = []) -> List[RaceInfo]:
        race_histories = []
        
        # リスティングページをクロールして物件詳細の URL 一覧を取得する
        #listing_page_url = self.race_info_listing_page_scraper.LISTING_PAGE_START_URLS
        page_count = 0
        while listing_page_url and page_count < crawl_limit: 
            listing_page = self.race_info_listing_page_scraper.get(listing_page_url)
            for_log = listing_page_url[:20] + "~" + listing_page_url[-20:]
            logger.info(
                f"listing_page_url: {for_log}, race_info_page_urls count: {len(listing_page.race_info_page_urls)}")

            # レース詳細ページにアクセスして、レースのデータを取得する
            for race_info_page_url in listing_page.race_info_page_urls:
                # CSV にアップロードするデータ構造をいれる
                # Errorが発生したら該当PropertyはSkipする
               
                if NETKEIBA_BASE_URL[:-1] + race_info_page_url in crawled_urls:
                    logger.info("already crawled. skip...")
                    return race_histories, None
                try:
                    if self._get_race_info(race_info_page_url):
                        race_histories.append(self._get_race_info(race_info_page_url))
                    else:
                        raise DetailPageNotFoundError("table not found.")
                except DetailPageNotFoundError as e:
                    logger.warning(f"Skip getting race:{e}")

            # if crawl_limit and len(race_histories) >= crawl_limit:
            #     # crawl_limit の件数に達したらクロールを終了する
            #     logger.info(f"Finish crawl. race_histories count: {len(race_histories)}")
            #     return race_histories, listing_page_url

            

            # next_page_url がある場合は次ページへアクセス
            listing_page_url = listing_page.next_page_url
            page_count += 1
            logger.info(f"crawled page count: {page_count}")
        
        logger.info(f"Finish crawl. race_histories count: {len(race_histories)}")
        return race_histories, listing_page_url

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

    def _check_crawled_urls(self):
        check_csvs = glob.glob("/Users/daikimiyazaki/workspace/pndnism/horse_race_prediction/horse_info_crawler/horse_info_crawler/race/data/race_histories/**/*.csv",recursive=True)
        concat_list = []
        if len(check_csvs) == 0:
            return []
        for i in check_csvs:
            concat_list.append(pd.read_csv(i))
        concat_df = pd.concat(concat_list, axis=0)
        crawled_urls = set(list(concat_df.race_url))
        del concat_df
        gc.collect()
        return list(crawled_urls)

    

