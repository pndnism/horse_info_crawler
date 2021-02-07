from dataclasses import dataclass
from horse_info_crawler.pedigree.normalizer import HorseInfoNormalizer
from horse_info_crawler.pedigree.domain import HorseInfo, ShapedHorseInfo
from typing import Type


@dataclass
class HorseInfoShaper:
    horse_info_normalizer: Type[HorseInfoNormalizer]

    def shape(self, horse_info: HorseInfo) -> ShapedHorseInfo:
        return ShapedHorseInfo(
            horse_url=self.horse_info_normalizer.normalize_horse_url(horse_info.horse_url),
            name=self.horse_info_normalizer.normalize_name(horse_info.name),
            birthday=self.horse_info_normalizer.normalize_birthday(horse_info.birthday),
            trainer_name=self.horse_info_normalizer.normalize_trainer_name(horse_info.trainer_name),
            owner_name=self.horse_info_normalizer.normalize_owner_name(horse_info.owner_name),
            producer=self.horse_info_normalizer.normalize_producer(horse_info.producer),
            origin_place=self.horse_info_normalizer.normalize_origin_place(horse_info.origin_place),
            mother=self.horse_info_normalizer.normalize_mother(horse_info.mother),
            father=self.horse_info_normalizer.normalize_father(horse_info.father),
            mother_of_father=self.horse_info_normalizer.normalize_mother_of_father(horse_info.mother_of_father),
            father_of_father=self.horse_info_normalizer.normalize_father_of_father(horse_info.father_of_father),
            mother_of_mother=self.horse_info_normalizer.normalize_mother_of_mother(horse_info.mother_of_mother),
            father_of_mother=self.horse_info_normalizer.normalize_father_of_mother(horse_info.father_of_mother)
        )