import csv
import dataclasses

from pandas.core.frame import DataFrame
from horse_info_crawler.race.domain import ShapedRaceData, ShapedRaceDetailInfo
import io
from datetime import datetime
from typing import Any, List
import os
import pandas as pd
import numpy as np

class DataFormatter:
    # TODO: この部分全体的に結構不格好。直したい。List[str]を連結してDataFrameにしてからそこに基礎データを追加していくようにしている
    def data_to_df(self, shaped_race_data_list: List[ShapedRaceData]) -> DataFrame:
        """
        ShapedRaceDataのリストをdataframeに変換する
        Args:
            shaped_race_info_list:
        Returns:
        """
        concat_list = []
        for shaped_race_data in shaped_race_data_list:
            elem_df = self.shaped_detail_info_list_to_df(shaped_race_data.shaped_race_detail_info)
            race_data_dict = shaped_race_data.shaped_race_info.__dict__
            for basic_info in race_data_dict.keys():
                elem_df[basic_info] = race_data_dict[basic_info]
            concat_list.append(elem_df)

        shaped_race_history_df = pd.concat(concat_list)
        return shaped_race_history_df

    def shaped_detail_info_list_to_df(self, shape_race_detail_info: ShapedRaceDetailInfo) -> DataFrame:
        elem_list = []
        for elem in shape_race_detail_info.__dict__.values():
            elem_list.append(elem)
        # TODO: np.arrayに変換してから転置してる、ちょっと不格好
        elem_list = np.array(elem_list).T
        shaped_detail_info_df = pd.DataFrame(elem_list, columns=shape_race_detail_info.__dict__.keys())
        return shaped_detail_info_df


@dataclasses.dataclass
class RaceInfoRepository:
    formatter: DataFormatter
    current_datetime: datetime

    def save_shaped_race_info(self, shaped_race_info_list: List[ShapedRaceData]):
        # shaped_race_data を dataframeに変換する
        df_data = self.formatter.data_to_df(shaped_race_info_list)
        current_date_ymd = self.current_datetime.strftime("%Y-%m-%d")
        current_time = self.current_datetime.now().time().strftime("%H%M%S")
        
        os.makedirs(f"./horse_info_crawler/race/data/race_histories/{current_date_ymd}", exist_ok=True)

        save_path = f"./horse_info_crawler/race/data/race_histories/{current_date_ymd}/shaped_race_history_{current_time}.csv"
        # データフレームを CSV として ローカルに保存する
        df_data.to_csv(save_path, index=False)

