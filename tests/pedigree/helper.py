import pandas as pd

from horse_info_crawler.pedigree.domain import HorseInfo, ShapedHorseInfo

def create_horse_info(i: int):
    return HorseInfo (
        horse_url=f'test_horse_url_{i}',
        name=f'test_name_{i}',
        birthday=f'test_birthday_{i}',
        trainer_name=f'test_trainer_name_{i}',
        owner_name=f'test_owner_name_{i}',
        producer=f'test_producer_{i}',
        origin_place=f'test_origin_place_{i}',
        mother=f'test_mother_{i}',
        father=f'test_father_{i}',
        mother_of_father=f'test_mother_of_father_{i}',
        father_of_father=f'test_father_of_father_{i}',
        mother_of_mother=f'test_mother_of_mother_{i}',
        father_of_mother=f'test_father_of_mother_{i}',
    )

def create_shaped_horse_data(i :int):
    return ShapedHorseInfo (
        horse_url=f'test_shaped_horse_url_{i}',
        name=f'test_shaped_name_{i}',
        birthday=f'test_shaped_birthday_{i}',
        trainer_name=f'test_shaped_trainer_name_{i}',
        owner_name=f'test_shaped_owner_name_{i}',
        producer=f'test_shaped_producer_{i}',
        origin_place=f'test_shaped_origin_place_{i}',
        mother=f'test_shaped_mother_{i}',
        father=f'test_shaped_father_{i}',
        mother_of_father=f'test_shaped_mother_of_father_{i}',
        father_of_father=f'test_shaped_father_of_father_{i}',
        mother_of_mother=f'test_shaped_mother_of_mother_{i}',
        father_of_mother=f'test_shaped_father_of_mother_{i}',
    )