from dataclasses import dataclass
from typing import Optional, List
from pandas import DataFrame

@dataclass(frozen=True)
class RaceInfo:
    # レース名
    name: str
    # 開催日
    date: str
    # 開催競馬場
    place: str
    # 開催NO.
    held_number: str
    # 競馬場開催日NO.
    held_date_number: str
    # コースタイプ
    course_type: str
    # 天候
    weather: str
    # 馬場状況
    course_condition: str
    # 備考
    remarks: Optional[str]
    # レース詳細情報
    race_details: DataFrame

@dataclass(frozen=True)
class ListingPage:
    next_page_post_parameter: Optional[str]
    next_page_element: Optional[str]
    race_info_page_urls: List[str]