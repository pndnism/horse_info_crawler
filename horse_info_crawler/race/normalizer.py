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
    def normalize_arrival_orders(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["着順"])

    @classmethod
    def normalize_box_numbers(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["枠番"])

    @classmethod
    def normalize_horse_numbers(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["馬番"])

    @classmethod
    def normalize_horse_names(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["馬名"])

    @classmethod
    def normalize_horse_ids(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["馬ID"])

    @classmethod
    def normalize_horse_sexes(cls, race_details: DataFrame) -> List[str]:
        race_details["sex"] = race_details["性齢"].replace("\d","",regex=True)
        return list(race_details["sex"])

    @classmethod
    def normalize_horse_ages(cls, race_details: DataFrame) -> List[str]:
        race_details["age"] = race_details["性齢"].str.extract("(\d+)")
        return list(race_details["age"])

    @classmethod
    def normalize_jockey_weights(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["斤量"])

    @classmethod
    def normalize_jockey_names(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["騎手"])

    @classmethod
    def normalize_goal_times(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["タイム"])

    @classmethod
    def normalize_goal_margins(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["着差"])

    @classmethod
    def normalize_order_transitions(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["通過"])

    @classmethod
    def normalize_half_times(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["上り"])

    @classmethod
    def normalize_odds(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["単勝"])

    @classmethod
    def normalize_popularities(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["人気"])

    @classmethod
    def normalize_horse_weights(cls, race_details: DataFrame) -> List[str]:
        race_details["horse_weight"] = race_details["馬体重"].str.extract("(\d+)")
        return list(race_details["horse_weight"])

    @classmethod
    def normalize_horse_weight_diffs(cls, race_details: DataFrame) -> List[str]:
        race_details["horse_weight_diff"] = race_details["馬体重"].str.extract("\((\W*\d+)\)")
        return list(race_details["horse_weight_diff"])

    @classmethod
    def normalize_trainer_names(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["調教師"])

    @classmethod
    def normalize_horse_owners(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["馬主"])

    @classmethod
    def normalize_earn_prizes(cls, race_details: DataFrame) -> List[str]:
        return list(race_details["賞金(万円)"])
