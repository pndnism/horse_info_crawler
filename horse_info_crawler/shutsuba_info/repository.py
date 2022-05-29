import csv
import dataclasses

from pandas.core.frame import DataFrame
from horse_info_crawler.shutsuba_info.domain import ShapedRaceData, ShapedRaceDetailInfo
from horse_info_crawler.shutsuba_info.config import SHUTUBA_RACE_INFO, PLACE_ID_DICT
import io
from datetime import datetime
from typing import Any, List
import os
import pandas as pd
import numpy as np

from google.cloud import storage
from horse_info_crawler.components import logger


class DataFormatter:
    # TODO:
    # この部分全体的に結構不格好。直したい。List[str]を連結してDataFrameにしてからそこに基礎データを追加していくようにしている
    def data_to_df(
            self,
            shaped_race_data: ShapedRaceData) -> DataFrame:
        """
        ShapedRaceDataのリストをdataframeに変換する
        Args:
            shaped_race_info_list:
        Returns:
        """

        elem_df = self.shaped_detail_info_list_to_df(
            shaped_race_data.shaped_race_detail_info)
        race_data_dict = shaped_race_data.shaped_race_info.__dict__
        for basic_info in race_data_dict.keys():
            elem_df[basic_info] = race_data_dict[basic_info]

        return elem_df

    def shaped_detail_info_list_to_df(
            self, shape_race_detail_info: ShapedRaceDetailInfo) -> DataFrame:
        elem_list = []
        for elem in shape_race_detail_info.__dict__.values():
            elem_list.append(elem)
        # TODO: np.arrayに変換してから転置してる、ちょっと不格好
        elem_list = np.array(elem_list).T
        shaped_detail_info_df = pd.DataFrame(
            elem_list, columns=shape_race_detail_info.__dict__.keys())
        return shaped_detail_info_df


@dataclasses.dataclass
class RaceInfoRepository:
    formatter: DataFormatter
    current_datetime: datetime

    def save_shaped_race_info(
            self,
            shaped_race_info_list: List[ShapedRaceData]):
        # shaped_race_data を dataframeに変換する
        df_data = self.formatter.data_to_df(shaped_race_info_list)
        # logger.info(df_data)
        if df_data.shape[0] == 0:
            logger.info("no data to save.")
            return
        # TODO 外だししたい
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/daikimiyazaki/.config/pndnism-project-fc40cb799b41.json'
        os.makedirs(
            f"./horse_info_crawler/race/data/predict_race_data/",
            exist_ok=True)
        _year = SHUTUBA_RACE_INFO["year"]
        place_id = ("0" + str(PLACE_ID_DICT[SHUTUBA_RACE_INFO["place"]]))[-2:]
        kaisu = ("0" + str(SHUTUBA_RACE_INFO["kaisu"]))[-2:]
        nichime = ("0" + str(SHUTUBA_RACE_INFO["nichime"]))[-2:]
        race_num = ("0" + str(SHUTUBA_RACE_INFO["race_num"]))[-2:]
        client = storage.Client()
        bucket = client.get_bucket('pndnism_horse_data')
        save_path = f"./horse_info_crawler/race/data/race_histories/{_year}{place_id}{kaisu}{nichime}{race_num}.csv"
        cs_save_path = f"predict_race_data/{_year}{place_id}{kaisu}{nichime}{race_num}.csv"
        # データフレームを CSV として ローカルに保存する
        df_data.to_csv(save_path, index=False)
        bucket.blob(cs_save_path).upload_from_string(
            df_data.to_csv(), 'text/csv')
