import csv
import dataclasses

from pandas.core.frame import DataFrame
from horse_info_crawler.race.domain import ShapedRaceData
import io
from datetime import datetime
from typing import Any, List
import os
import pandas as pd

class DataFormatter:
    def data_to_df(self, shaped_race_data_list: List[ShapedRaceData]) -> DataFrame:
        """
        ShapedRaceDataのリストをdataframeに変換する
        Args:
            shaped_race_info_list:
        Returns:
        """
        concat_list = []
        for shaped_race_data in shaped_race_data_list:
            elem_df = shaped_race_data.shaped_race_detail_info
            for basic_info in shaped_race_data.shaped_race_info.__dict__.keys:
                elem_df[basic_info] = shaped_race_data.shaped_race_info.__dict__[basic_info]
            concat_list.append(elem_df)

        shaped_race_history_df = pd.concat(concat_list)
        return shaped_race_history_df

    def _dict_to_csv(self, header: List[str], rows: List[dict]):
        with io.StringIO() as f:
            writer = csv.DictWriter(f, header, lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            return f.getvalue()


@dataclasses.dataclass
class PropertyDataRepository:
    formatter: DataFormatter
    crawled_data_base_dir: str
    target_crawled_data_base_dir: str
    current_datetime: datetime

    def save_shaped_properties(self, shaped_race_info_list: List[ShapedRaceData]):
        # shaped_race_data を dataframeに変換する
        df_data = self.formatter.data_to_df(shaped_race_info_list)
        current_date_ymd = self.current_datetime.strftime("%Y/%m/%d")
        
        os.makedirs(f"../../data/race_histories/{current_date_ymd}", exist_ok=True)

        save_path = f"../../data/race_histories/{current_date_ymd}/shaped_race_history.csv"
        # データフレームを CSV として ローカルに保存する
        df_data.to_csv(save_path, index=False)