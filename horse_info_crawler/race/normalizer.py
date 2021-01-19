import re
from types import ClassMethodDescriptorType
from typing import List
from pandas.core.frame import DataFrame


class UnsupportedFormatError(Exception):
    """
    対応していないフォーマットのデータが入力された時のエラー
    """
    pass


class InvalidFormatError(Exception):
    """
    想定していないフォーマットのデータが入力された時のエラー
    """
    pass


class RaceInfoNormalizer:
    @classmethod
    def normalize_name(cls, name: str) -> str:
        return name

    @classmethod
    def normalize_race_number(cls, race_number: str) -> str:
        return re.findall(r'(\d+)\sR', race_number)[0]

    @classmethod
    def normalize_course_type(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[0]
        return re.search("ダ|芝|障芝", elem).group()

    @classmethod
    def normalize_course_direction(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[0]
        return re.search("右|左|直線|ダート|外|内-外|外-内|内2周", elem).group()

    @classmethod
    def normalize_course_length(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[0]
        return re.search("[0-9]{2,5}", elem).group()

    @classmethod
    def normalize_weather(cls, course_run_info: str) -> str:
        if "天候" in course_run_info:
            elem = course_run_info.split(" / ")[1]
            return re.split(' : ', elem)[1]
        
        raise InvalidFormatError(f'Invalid format. : {course_run_info}')
        
    @classmethod
    def normalize_course_condition(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[2]
        return re.split(' : ', elem)[1]

    @classmethod
    def normalize_race_start_time(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[3]
        return re.split(' : ', elem)[1]

    @classmethod
    def normalize_held_date(cls, held_info: str) -> str:
        elem = held_info.split(" ")[0]
        return elem

    @classmethod
    def normalize_held_place(cls, held_info: str) -> str:
        elem = held_info.split(" ")[1]
        return re.sub("[[0-9]+回|[0-9]+日目","",elem)

    @classmethod
    def normalize_held_number(cls, held_info: str) -> str:
        elem = held_info.split(" ")[1]
        return re.findall("(\d+)回", elem)[0]

    @classmethod
    def normalize_held_date_number(cls, held_info: str) -> str:
        elem = held_info.split(" ")[1]
        return re.findall("(\d+)日目", elem)[0]

    @classmethod
    def normalize_explanation(cls, held_info: str) -> str:
        return "".join(held_info.split(" ")[2:])


class RaceDetailsNormalizer:
    @classmethod
    def normalize_arrival_orders(cls, arrival_orders: List[str]) -> List[str]:
        return [i.text for i in arrival_orders]

    @classmethod
    def normalize_box_numbers(cls, box_numbers: List[str]) -> List[str]:
        return [i.text for i in box_numbers]

    @classmethod
    def normalize_horse_numbers(cls, horse_numbers: List[str]) -> List[str]:
        return [i.text for i in horse_numbers]

    @classmethod
    def normalize_horse_names(cls, horse_info: List[str]) -> List[str]:
        raw_list = [i.text for i in horse_info]
        return [raw.replace("\n", "") for raw in raw_list]

    @classmethod
    def normalize_horse_ids(cls, horse_info: List[str]) -> List[str]:
        raw_list = [i.find("a").get("href") for i in horse_info]
        return [re.findall("(\d+)", raw)[0] for raw in raw_list]

    @classmethod
    def normalize_horse_sexes(cls, horse_ages_and_sexes: List[str]) -> List[str]:
        return [re.findall("(セ|牝|牡)",i.text)[0] for i in horse_ages_and_sexes]

    @classmethod
    def normalize_horse_ages(cls, horse_ages_and_sexes: List[str]) -> List[str]:
        return [re.findall("(\d+)",i.text)[0] for i in horse_ages_and_sexes]

    @classmethod
    def normalize_jockey_weights(cls, jockey_weights: List[str]) -> List[str]:
        return [re.findall("(\d+)",i.text)[0] for i in jockey_weights]

    @classmethod
    def normalize_jockey_names(cls, jockey_names: List[str]) -> List[str]:
        raw_list = [i.text for i in jockey_names]
        return [raw.replace("\n", "") for raw in raw_list]

    @classmethod
    def normalize_goal_times(cls, goal_times: List[str]) -> List[str]:
        return [i.text for i in goal_times]

    @classmethod
    def normalize_goal_margins(cls, goal_margins: List[str]) -> List[str]:
        return [i.text for i in goal_margins]

    @classmethod
    def normalize_order_transitions(cls, order_transitions: List[str]) -> List[str]:
        return [i.text for i in order_transitions]

    @classmethod
    def normalize_half_times(cls, half_times: List[str]) -> List[str]:
        return [i.text for i in half_times]

    @classmethod
    def normalize_odds(cls, odds: List[str]) -> List[str]:
        return [i.text for i in odds]

    @classmethod
    def normalize_popularities(cls, popularities: List[str]) -> List[str]:
        return [i.text for i in popularities]

    @classmethod
    def normalize_horse_weights(cls, horse_weights: List[str]) -> List[str]:
        raw_list = [i.text for i in horse_weights]
        return [re.findall("(\d+)\(",raw)[0] if "計不" not in raw else None for raw in raw_list]

    @classmethod
    def normalize_horse_weight_diffs(cls, horse_weights: List[str]) -> List[str]:
        if "計不" in horse_weights:
            return None
        raw_list = [i.text for i in horse_weights]
        return [re.findall("[(]([\+|\-]\d+|0)[)]",raw)[0] 
                    if "計不" not in raw else None for raw in raw_list]

    @classmethod
    def normalize_trainer_names(cls, trainer_names: List[str]) -> List[str]:
        raw_list = [i.text for i in trainer_names]
        return [raw.replace("\n", "") for raw in raw_list]

    @classmethod
    def normalize_horse_owners(cls, horse_owners: List[str]) -> List[str]:
        raw_list = [i.text for i in horse_owners]
        return [raw.replace("\n", "") for raw in raw_list]

    @classmethod
    def normalize_earn_prizes(cls, earn_prizes: List[str]) -> List[str]:
        return [i.text for i in earn_prizes]
