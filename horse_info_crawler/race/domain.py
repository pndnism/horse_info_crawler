from dataclasses import dataclass
from typing import Optional, List
from pandas.core.frame import DataFrame

@dataclass(frozen=True)
class RaceInfo:
    # レース名
    name: str
    # レースNO.
    race_number: str
    # コース/発走情報
    course_run_info: str
    # 開催情報
    held_info: str
    # レース詳細情報
    race_details: DataFrame

@dataclass(frozen=True)
class ListingPage:
    next_page_post_parameter: Optional[str]
    next_page_element: Optional[str]
    race_info_page_urls: List[str]

@dataclass(frozen=True)
class ShapedRaceInfo:
    # レース名
    name: str
    # レースNO.
    race_number: str
    # コースタイプ（芝, ダート..）
    course_type: str
    # コースの向き
    course_direction: str
    # コース長
    course_length: str
    # 天気
    weather: str
    # コースコンディション
    course_condition: str
    # 発走時刻
    race_start_time: str
    # 開催日
    held_date: str
    # 開催競馬場
    held_place: str
    # 開催No.（~回）
    held_number: str
    # 開催日目（~日目）
    held_date_number: str
    # 備考
    explanation: str
    # レース詳細情報
    race_details: DataFrame

@dataclass(frozen=True)
class ShapedRaceDetailInfo:
    # 着順
    arrival_order: str
    # 枠番
    box_number: str
    # 馬番
    horse_number: str
    # 馬名
    horse_name: str
    # 性別
    horse_sex: str
    # 年齢
    horse_age: str
    # 斤量
    jockey_weight: str
    # 騎手
    jockey_name: str
    # タイム
    goal_time: str
    # 着差
    goal_margin: str
    # 通過
    order_transition: str
    # 上り
    half_time: str
    # 単勝オッズ
    odds: str
    # 人気
    popularity: str
    # 馬体重
    horse_weight: str
    # 馬体重変化
    horse_weight_diff: str
    # 調教師
    trainer_name: str
    # 馬主
    horse_owner: str
    # 賞金
    earn_prize: str