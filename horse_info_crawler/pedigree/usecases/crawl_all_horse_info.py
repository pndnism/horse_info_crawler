from dataclasses import dataclass
from os import name
import urllib
from horse_info_crawler.pedigree.repository import HorseInfoRepository
from horse_info_crawler.pedigree.normalizer import InvalidFormatError, UnsupportedFormatError
from urllib.parse import urlencode
import glob
import pandas as pd
from horse_info_crawler.pedigree.domain import HorseInfo, ShapedHorseInfo
from typing import Optional, List
from horse_info_crawler.pedigree.shaper import HorseInfoShaper
from horse_info_crawler.pedigree.scraper import DetailPageNotFoundError, NETKEIBA_BASE_URL, HorseInfoListingPageScraper, HorseInfoScraper
from horse_info_crawler.components import logger
import time

@dataclass
class CrawlHorseInfoUsecase:
    horse_info_listing_page_scraper: HorseInfoListingPageScraper
    horse_info_scraper: HorseInfoScraper
    horse_info_shaper: HorseInfoShaper
    horse_info_repository: HorseInfoRepository

    def exec(self, crawl_limit: Optional[int] = None):
        logger.info(f'Start crawl_horse_info. crawl_limit: {crawl_limit}')
        horse_info = self._crawl_horse_info(crawl_limit)

        # horse_histories を CSV に変換して ローカルに保存する
        self.horse_info_repository.save_shaped_horse_info(self._shape_horse_infos(horse_info))
        logger.info("End crawl_horse_info.")

    def _prepare_to_check_saved_urls():
        pass
    
    def _crawl_horse_info(self, crawl_limit: Optional[int] = None) -> List[HorseInfo]:
        horse_info = []
        crawled_urls = self._check_crawled_urls()
        # リスティングページをクロールして物件詳細の URL 一覧を取得する
        listing_page_url = self.horse_info_listing_page_scraper.LISTING_PAGE_START_URLS
        count = 0
        while listing_page_url:
            listing_page = self.horse_info_listing_page_scraper.get(listing_page_url)
            for_log = listing_page_url[:20] + "~" + listing_page_url[-20:]
            logger.info(
                f"listing_page_url: {for_log}, horse_info_page_urls count: {len(listing_page.horse_info_page_urls)}")

            # レース詳細ページにアクセスして、レースのデータを取得する
            for horse_info_page_url in listing_page.horse_info_page_urls:
                # CSV にアップロードするデータ構造をいれる
                # Errorが発生したら該当PropertyはSkipする
                count += 1
                if NETKEIBA_BASE_URL[:-1] + horse_info_page_url in crawled_urls:
                    logger.info("already crawled. skip...")
                    continue
                try:
                    if self._get_horse_info(horse_info_page_url):
                        horse_info.append(self._get_horse_info(horse_info_page_url))
                    else:
                        raise DetailPageNotFoundError("table not found.")
                except DetailPageNotFoundError as e:
                    logger.warning(f"Skip getting horse:{e}")
                    # TODO: sentryとかエラー監視ツール入れる

                #if count == 100:
                    #logger.info("10sec crawler idling... ")
                    #time.sleep(10)
                #    count = 0
                if crawl_limit and len(horse_info) >= crawl_limit:
                    # crawl_limit の件数に達したらクロールを終了する
                    logger.info(f"Finish crawl. horse_histories count: {len(horse_info)}")
                    return horse_info

            # next_page_url がある場合は次ページへアクセス
            print(listing_page.next_page_url)
            listing_page_url = listing_page.next_page_url 
        
        logger.info(f"Finish crawl. horse_histories count: {len(horse_info)}")
        return horse_info

    def _get_horse_info(self, horse_info_url: str) -> HorseInfo:
            """
            レースのクロールをして rawデータを返す
            Args:
                horse_info_url:
            Returns:
            """
            horse_info = self.horse_info_scraper.get(horse_info_url)

            # CSV にアップロードするデータ構造をいれる
            return horse_info

    def _shape_horse_infos(self, horse_info_list: List[HorseInfo]) -> List[ShapedHorseInfo]:
        shaped_horse_info_list = []
        for horse_info in horse_info_list:
            try:
                # Error が発生したら該当 HorseInfo は Skip する
                shaped_horse_info_list.append(self._shape_horse_info(horse_info))
            except UnsupportedFormatError as e:
                logger.info(f"Skip getting horse info:{e}")
                # TODO: エラー検知をsentryとかで実装する
            except InvalidFormatError as e:
                logger.warning(f"Skip getting horse info:{e}")
                # TODO: エラー検知をsentryとかで実装する

        return shaped_horse_info_list

    def _shape_horse_info(self, horse_info: HorseInfo) -> ShapedHorseInfo:
        return self.horse_info_shaper.shape(horse_info)

    def _check_crawled_urls(self):
        check_csvs = glob.glob("/Users/daikimiyazaki/workspace/pndnism/horse_race_prediction/horse_info_crawler/horse_info_crawler/pedigree/data/horse_info/**/*.csv",recursive=True)
        concat_list = []
        if len(check_csvs) == 0:
            return []
        for i in check_csvs:
            concat_list.append(pd.read_csv(i))
        concat_df = pd.concat(concat_list, axis=0)
        crawled_urls = set(list(concat_df.horse_url))
        return list(crawled_urls)

    

