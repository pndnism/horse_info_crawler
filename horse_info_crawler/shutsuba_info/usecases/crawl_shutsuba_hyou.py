from dataclasses import dataclass
from os import name
from horse_info_crawler.shutsuba_info.repository import RaceInfoRepository
from horse_info_crawler.shutsuba_info.normalizer import InvalidFormatError, UnsupportedFormatError
from urllib.parse import urlencode
import glob
import pandas as pd
from horse_info_crawler.shutsuba_info.domain import RaceInfo, ShapedRaceData
from typing import Optional, List
from horse_info_crawler.shutsuba_info.shaper import RaceInfoShaper
from horse_info_crawler.shutsuba_info.scraper import DetailPageNotFoundError, NETKEIBA_BASE_URL, RaceInfoScraper
from horse_info_crawler.components import logger
from google.cloud import storage
import re
from horse_info_crawler.shutsuba_info.config import SHUTUBA_RACE_INFO, PLACE_ID_DICT


@dataclass
class CrawlShutsubaHyouUsecase:
    race_info_scraper: RaceInfoScraper
    race_info_shaper: RaceInfoShaper
    race_info_repository: RaceInfoRepository

    def exec(self):
        _year = SHUTUBA_RACE_INFO["year"]
        place_id = ("0" + str(PLACE_ID_DICT[SHUTUBA_RACE_INFO["place"]]))[-2:]
        kaisu = ("0" + str(SHUTUBA_RACE_INFO["kaisu"]))[-2:]
        nichime = ("0" + str(SHUTUBA_RACE_INFO["nichime"]))[-2:]
        race_num = ("0" + str(SHUTUBA_RACE_INFO["race_num"]))[-2:]
        race_info_url = f"{NETKEIBA_BASE_URL}race/shutuba.html?race_id={_year}{place_id}{kaisu}{nichime}{race_num}"
        race_info = self._get_race_info(race_info_url)
        # logger.info(f"race_info: {race_info}")
        self.race_info_repository.save_shaped_race_info(
            self._shape_race_info(race_info))
        logger.info("End crawl_race_histories.")

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

    def _shape_race_info(
            self,
            race_info: RaceInfo) -> ShapedRaceData:
        try:
            # Error が発生したら該当 RaceInfo は Skip する
            shaped_race_info = self.race_info_shaper.shape(race_info)
        except UnsupportedFormatError as e:
            logger.info(f"Skip getting race info:{e}")
            return None
        except InvalidFormatError as e:
            logger.warning(f"Skip getting race info:{e}")
            return None

        return shaped_race_info
