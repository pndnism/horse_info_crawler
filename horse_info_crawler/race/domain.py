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