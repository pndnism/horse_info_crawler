
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ListingPage:
    next_page_url: Optional[str]
    horse_info_page_urls: List[str]

@dataclass(frozen=True)
class HorseInfo:
    name: str
    birthday: Optional[str]
    trainer_name: Optional[str]
    owner_name: Optional[str]
    producer: Optional[str]
    origin_place: Optional[str]
    mother: str
    father: str
    mother_of_father: str
    father_of_father: str
    mother_of_mother: str
    father_of_mother: str


@dataclass(frozen=True)
class ShapedHorseInfo:
    name: str
    birthday: Optional[str]
    trainer_name: Optional[str]
    owner_name: Optional[str]
    producer: Optional[str]
    origin_place: Optional[str]
    mother: str
    father: str
    mother_of_father: str
    father_of_father: str
    mother_of_mother: str
    father_of_mother: str
