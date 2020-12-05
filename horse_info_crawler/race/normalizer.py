import re
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
        return re.find(r'(\d+)\sR', race_number)

    @classmethod
    def normalize_course_type(cls, name: str) -> str:
        pass

    @classmethod
    def normalize_course_direction(cls, course_run_info: str) -> str:
        pass

    @classmethod
    def normalize_course_length(cls, course_run_info: str) -> str:
        pass

    @classmethod
    def normalize_weather(cls, course_run_info: str) -> str:
        pass

    @classmethod
    def normalize_course_condition(cls, course_run_info: str) -> str:
        pass

    @classmethod
    def normalize_race_start_time(cls, course_run_info: str) -> str:
        pass

    @classmethod
    def normalize_held_date(cls, held_info: str) -> str:
        pass

    @classmethod
    def normalize_held_place(cls, held_info: str) -> str:
        pass

    @classmethod
    def normalize_held_number(cls, held_info: str) -> str:
        pass

    @classmethod
    def normalize_held_date_number(cls, held_info: str) -> str:
        pass

    @classmethod
    def normalize_explanation(cls, held_info: str) -> str:
        pass

class RaceDetailsNormalizer:
    @classmethod
    def normalize_arrival_orders(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_box_numbers(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_numbers(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_names(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_sexes(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_ages(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_jockey_names(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_goal_times(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_goal_margins(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_order_transitions(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_half_times(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_odds(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_popularities(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_weights(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_weight_diffs(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_trainer_names(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_horse_owners(cls, race_details: DataFrame) -> List[str]:
        pass

    @classmethod
    def normalize_earn_prizes(cls, race_details: DataFrame) -> List[str]:
        pass