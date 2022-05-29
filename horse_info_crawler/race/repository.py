import csv
import dataclasses

from pandas.core.frame import DataFrame
from horse_info_crawler.race.domain import PayResult, ShapedPayResult, ShapedRaceData, ShapedRaceDetailInfo
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
            shaped_race_data_list: List[ShapedRaceData]) -> DataFrame:
        """
        ShapedRaceDataのリストをdataframeに変換する
        Args:
            shaped_race_info_list:
        Returns:
        """
        concat_list = []
        for shaped_race_data in shaped_race_data_list:
            elem_df = self.shaped_detail_info_list_to_df(
                shaped_race_data.shaped_race_detail_info)
            race_data_dict = shaped_race_data.shaped_race_info.__dict__
            for basic_info in race_data_dict.keys():
                elem_df[basic_info] = race_data_dict[basic_info]
            concat_list.append(elem_df)
        if len(concat_list) == 0:
            return pd.DataFrame()
        shaped_race_history_df = pd.concat(concat_list)
        shaped_race_history_df["cross_join_key"] = "x"
        pay_result_df = self.pay_result_to_df(
            shaped_race_data.shaped_pay_result)
        if pay_result_df.shape[0] == 0:
            return shaped_race_history_df
        shaped_race_history_df = shaped_race_history_df.merge(
            pay_result_df, how="left", on="cross_join_key")
        shaped_race_history_df.drop("cross_join_key", axis=1, inplace=True)
        return shaped_race_history_df

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

    def pay_result_to_df(
            self,
            shaped_pay_result: ShapedPayResult) -> DataFrame:
        if not shaped_pay_result:
            return pd.DataFrame()
        df = pd.DataFrame(shaped_pay_result.__dict__, index=[0])
        df["cross_join_key"] = "x"
        return df


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
        current_date_ymd = self.current_datetime.strftime("%Y-%m-%d")
        current_time = self.current_datetime.now().time().strftime("%H%M%S")
        # TODO 外だししたい
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/daikimiyazaki/.config/pndnism-project-fc40cb799b41.json'
        os.makedirs(
            f"./horse_info_crawler/race/data/race_histories/{current_date_ymd}",
            exist_ok=True)

        client = storage.Client()
        bucket = client.get_bucket('pndnism_horse_data')
        save_path = f"./horse_info_crawler/race/data/race_histories/{current_date_ymd}/shaped_race_history_{current_time}.csv"
        cs_save_path = f"race_histories/{current_date_ymd}/shaped_race_history_{current_time}.csv"
        # データフレームを CSV として ローカルに保存する
        df_data.to_csv(save_path, index=False)
        bucket.blob(cs_save_path).upload_from_string(
            df_data.to_csv(), 'text/csv')
