import csv
import dataclasses

from pandas.core.frame import DataFrame
from horse_info_crawler.pedigree.domain import ShapedHorseInfo
import io
from datetime import datetime
from typing import Any, List
import os
import pandas as pd
import numpy as np

from google.cloud import storage

class DataFormatter:
    # TODO: この部分全体的に結構不格好。直したい。List[str]を連結してDataFrameにしてからそこに基礎データを追加していくようにしている
    def data_to_df(self, shaped_horse_info_list: List[ShapedHorseInfo]) -> DataFrame:
        """
        ShapedHorseInfoのリストをdataframeに変換する
        Args:
            shaped_horse_info_list:
        Returns:
        """
        concat_list = []
        for shaped_horse_info in shaped_horse_info_list:
            horse_data_dict = shaped_horse_info.__dict__
            concat_list.append(horse_data_dict)

        shaped_horse_info_df = pd.DataFrame(concat_list)
        return shaped_horse_info_df

@dataclasses.dataclass
class HorseInfoRepository:
    formatter: DataFormatter
    current_datetime: datetime

    def save_shaped_horse_info(self, shaped_horse_info_list: List[ShapedHorseInfo]):
        # shaped_horse_data を dataframeに変換する
        df_data = self.formatter.data_to_df(shaped_horse_info_list)
        current_date_ymd = self.current_datetime.strftime("%Y-%m-%d")
        current_time = self.current_datetime.now().time().strftime("%H%M%S")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/daikimiyazaki/.config/pndnism-project-fc40cb799b41.json'
        os.makedirs(f"./horse_info_crawler/pedigree/data/horse_info/{current_date_ymd}", exist_ok=True)

        client = storage.Client()
        bucket = client.get_bucket('pndnism_horse_data')
        save_path = f"./horse_info_crawler/pedigree/data/horse_info/{current_date_ymd}/shaped_horse_info_{current_time}.csv"
        cs_save_path = f"pedigree/data/horse_info/{current_date_ymd}/shaped_horse_info_{current_time}.csv"
        # データフレームを CSV として ローカルに保存する
        df_data.to_csv(save_path, index=False)
        bucket.blob(cs_save_path).upload_from_string(df_data.to_csv(), 'text/csv')

