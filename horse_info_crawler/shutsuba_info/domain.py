from dataclasses import dataclass
from typing import Optional, List
from pandas.core.frame import DataFrame


@dataclass(frozen=True)
class RaceDetailInfo:
    # 枠番
    box_numbers: List[str]
    # 馬番
    horse_numbers: List[str]
    # 馬情報
    horse_info: List[str]
    # 年齢&性別
    horse_ages_and_sexes: List[str]
    # 斤量
    jockey_weights: List[str]
    # 騎手
    jockey_names: List[str]
    # 単勝オッズ TODO: seleniumを使ってとる
    # odds: List[str]
    # 人気 TODO: seleniumを使ってとる
    popularities: List[str]
    # 馬体重
    horse_weights: List[str]
    # 調教師
    trainer_names: List[str]
    # 馬ID
    horse_ids: List[str]


@dataclass
class PayResult:
    # 単勝
    tansho: List[List[str]]
    # 複勝
    fukusho: List[List[str]]
    # 馬連
    umaren: List[List[str]]
    # ワイド
    wide: List[List[str]]
    # 馬単
    umatan: List[List[str]]
    # 三連複
    sanrentan: List[List[str]]
    # 三連単
    sanrenpuku: List[List[str]]


@dataclass(frozen=True)
class RaceInfo:
    # レースURL
    race_url: str
    # レース名
    name: str
    # レースNO.
    race_number: str
    # コース/発走情報
    course_run_info: str
    # 開催日
    held_date: str
    # 開催情報
    held_info: str
    # レース詳細情報
    race_detail_info: RaceDetailInfo


@dataclass(frozen=True)
class ListingPage:
    next_page_url: Optional[str]
    race_info_page_urls: List[str]


@dataclass(frozen=True)
class ShapedRaceInfo:
    # レースURL
    race_url: str
    # レース名
    name: str
    # レースNO.
    race_number: str
    # コースタイプ（芝, ダート..）
    course_type: str
    # コースの向き
    course_direction: str
    # コース長（単位: m）
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


@dataclass(frozen=True)
class ShapedRaceDetailInfo:
    # 枠番
    box_numbers: List[str]
    # 馬番
    horse_numbers: List[str]
    # 馬名
    horse_names: List[str]
    # 馬ID
    horse_ids: List[str]
    # 性別
    horse_sexes: List[str]
    # 年齢
    horse_ages: List[str]
    # 斤量
    jockey_weights: List[str]
    # 騎手
    jockey_names: List[str]
    # # 単勝オッズ
    # odds: List[str]
    # 人気
    popularities: List[str]
    # 馬体重
    horse_weights: List[str]
    # 馬体重変化
    horse_weight_diffs: List[str]
    # 調教師
    trainer_names: List[str]
    # # 馬主
    # horse_owners: List[str]


@dataclass
class ShapedRaceData:
    shaped_race_info: ShapedRaceInfo
    shaped_race_detail_info: ShapedRaceDetailInfo
