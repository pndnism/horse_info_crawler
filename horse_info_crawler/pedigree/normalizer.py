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

class HorseInfoNormalizer:
    @classmethod
    def normalize_horse_url(cls, horse_url: str) -> str:
        return horse_url
    
    @classmethod
    def normalize_name(cls, name: str) -> str:
        return name
    
    @classmethod
    def normalize_birthday(cls, birthday: str) -> str:
        return birthday
    
    @classmethod
    def normalize_trainer_name(cls, trainer_name: str) -> str:
        return trainer_name
    
    @classmethod
    def normalize_owner_name(cls, owner_name: str) -> str:
        return owner_name
    
    @classmethod
    def normalize_producer(cls, producer: str) -> str:
        return producer
    
    @classmethod
    def normalize_origin_place(cls, origin_place: str) -> str:
        return origin_place
    
    @classmethod
    def normalize_mother(cls, mother: str) -> str:
        return mother
    
    @classmethod
    def normalize_father(cls, father: str) -> str:
        return father
    
    @classmethod
    def normalize_mother_of_father(cls, mother_of_father: str) -> str:
        return mother_of_father
    
    @classmethod
    def normalize_father_of_father(cls, father_of_father: str) -> str:
        return father_of_father
    
    @classmethod
    def normalize_mother_of_mother(cls, mother_of_mother: str) -> str:
        return mother_of_mother
    
    @classmethod
    def normalize_father_of_mother(cls, father_of_mother: str) -> str:
        return father_of_mother
