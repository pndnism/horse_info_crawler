from horse_info_crawler.components import logger
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
    def normalize_race_url(cls, race_url: str) -> str:
        return race_url

    @classmethod
    def normalize_name(cls, name: str) -> str:
        return name

    @classmethod
    def normalize_race_number(cls, race_number: int) -> str:
        if race_number is None:
            return

        return str(race_number)

    @classmethod
    def normalize_course_type(cls, course_run_info: str) -> str:
        if course_run_info is not None:
            elem = course_run_info.split(" / ")[1]
            if elem is None:
                return None
            return re.search("ダ|芝|障芝", elem).group()

        raise InvalidFormatError(f'Invalid format. : {course_run_info}')

    @classmethod
    def normalize_course_direction(cls, course_run_info: str) -> str:
        if course_run_info is not None:

            elem = course_run_info.split(" / ")[1]
            if elem is None:
                return None
            return re.search("右|左|直線|ダート|外|内-外|外-内|内2周", elem).group()

        raise InvalidFormatError(f'Invalid format. : {course_run_info}')

    @classmethod
    def normalize_course_length(cls, course_run_info: str) -> str:
        if course_run_info is not None:
            elem = course_run_info.split(" / ")[1]
            if elem is None:
                return None
            if re.search("[0-9]{2,5}", elem) is None:
                return None

            return re.search("[0-9]{2,5}", elem).group()

        raise InvalidFormatError(f'Invalid format. : {course_run_info}')

    @classmethod
    def normalize_weather(cls, course_run_info: str) -> str:
        if "天候" in course_run_info:
            elem = course_run_info.split(" / ")[2]
            # TODO: 天候の一覧リストから判定できそう。
            if elem is None:
                return None
            if len(re.split(':', elem)) < 2:
                return None
            return re.split(':', elem)[1]
        else:
            logger.warning("天気情報が存在しません")
            return None

    @classmethod
    def normalize_course_condition(cls, course_run_info: str) -> str:
        if len(course_run_info.split(" / ")) < 3:
            return None
        elem = course_run_info.split(" / ")[3]
        if elem is None:
            return None
        if len(re.split(':', elem)) < 2:
            return None
        return re.split(':', elem)[1]

    @classmethod
    def normalize_race_start_time(cls, course_run_info: str) -> str:
        elem = course_run_info.split(" / ")[0]
        if elem is None:
            return None
        return re.search(r"\d{2}\:\d{2}", elem).group()

    @classmethod
    def normalize_held_date(cls, held_info: str) -> str:
        return held_info

    @classmethod
    def normalize_explanation(cls, held_info: str) -> str:
        return "".join(held_info.split(" ")[2:])


class RaceDetailsNormalizer:

    @classmethod
    def normalize_box_numbers(cls, box_numbers: List[str]) -> List[str]:
        return [str(i) for i in box_numbers]

    @classmethod
    def normalize_horse_numbers(cls, horse_numbers: List[str]) -> List[str]:
        return [str(i) for i in horse_numbers]

    @classmethod
    def normalize_horse_names(cls, horse_info: List[str]) -> List[str]:
        return [raw.replace("\n", "") for raw in horse_info]

    @classmethod
    def normalize_horse_ids(cls, horse_ids: List[str]) -> List[str]:
        return horse_ids

    @classmethod
    def normalize_horse_sexes(
            cls, horse_ages_and_sexes: List[str]) -> List[str]:
        return [re.findall("(セ|牝|牡)", i)[0]
                if len(re.findall("(セ|牝|牡)", i)) != 0
                else None for i in horse_ages_and_sexes]

    @classmethod
    def normalize_horse_ages(
            cls, horse_ages_and_sexes: List[str]) -> List[str]:
        return [re.findall(r"(\d+)", i)[0]
                if len(re.findall(r"(\d+)", i)) != 0
                else None for i in horse_ages_and_sexes]

    @classmethod
    def normalize_jockey_weights(cls, jockey_weights: List[str]) -> List[str]:
        return [str(i) if i else None for i in jockey_weights]

    @classmethod
    def normalize_jockey_names(cls, jockey_names: List[str]) -> List[str]:
        raw_list = [i for i in jockey_names]
        return [raw.replace("\n", "") for raw in raw_list]

    @classmethod
    def normalize_odds(cls, odds: List[str]) -> List[str]:
        return [i for i in odds]

    @classmethod
    def normalize_popularities(cls, popularities: List[str]) -> List[str]:
        return [i for i in popularities]

    @classmethod
    def normalize_horse_weights(cls, horse_weights: List[str]) -> List[str]:
        if horse_weights[0] != horse_weights[0]:
            return [None for i in horse_weights]
        return [
            re.findall(
                r"(\d+)\(",
                raw)[0] if "計不" not in raw and len(
                re.findall(
                    r"(\d+)\(",
                    raw)) >= 1 else None for raw in horse_weights]

    @classmethod
    def normalize_horse_weight_diffs(
            cls, horse_weights: List[str]) -> List[str]:
        if horse_weights[0] != horse_weights[0]:
            return [None for i in horse_weights]
        if "計不" in horse_weights:
            return None
        return [
            re.findall(
                r"[(]([\+|\-]\d+|0)[)]",
                raw)[0] if "計不" not in raw and len(
                re.findall(
                    r"[(]([\+|\-]\d+|0)[)]",
                    raw)) >= 1 else None for raw in horse_weights]

    @classmethod
    def normalize_trainer_names(cls, trainer_names: List[str]) -> List[str]:
        return [raw.replace("\n", "") for raw in trainer_names]

    @classmethod
    def normalize_horse_owners(cls, horse_owners: List[str]) -> List[str]:
        # TODO: 馬主名が取れてない。どっか取れるとこあるか探す。というか馬主って変わることあるのか？
        return [raw.replace("\n", "") for raw in horse_owners]
