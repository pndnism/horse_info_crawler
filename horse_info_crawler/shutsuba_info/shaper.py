from dataclasses import dataclass
from horse_info_crawler.components import logger
from horse_info_crawler.shutsuba_info.config import SHUTUBA_RACE_INFO
from horse_info_crawler.shutsuba_info.normalizer import RaceDetailsNormalizer, RaceInfoNormalizer
from horse_info_crawler.shutsuba_info.domain import RaceDetailInfo, RaceInfo, ShapedRaceData, ShapedRaceDetailInfo, ShapedRaceInfo
from typing import Type


@dataclass
class RaceInfoShaper:
    race_info_normalizer: Type[RaceInfoNormalizer]
    race_details_normalizer: Type[RaceDetailsNormalizer]

    def shape(self, race_info: RaceInfo) -> ShapedRaceData:
        return ShapedRaceData(
            shaped_race_info=self.shape_race_info(race_info),
            shaped_race_detail_info=self.shape_race_detail_info(
                race_info.race_detail_info),
        )

    def shape_race_info(self, race_info: RaceInfo):
        return ShapedRaceInfo(
            race_url=self.race_info_normalizer.normalize_race_url(
                race_info.race_url),
            name=self.race_info_normalizer.normalize_name(race_info.name),
            race_number=self.race_info_normalizer.normalize_race_number(
                race_info.race_number),
            course_type=self.race_info_normalizer.normalize_course_type(
                race_info.course_run_info),
            course_direction=self.race_info_normalizer.normalize_course_direction(
                race_info.course_run_info),
            course_length=self.race_info_normalizer.normalize_course_length(
                race_info.course_run_info),
            weather=self.race_info_normalizer.normalize_weather(
                race_info.course_run_info),
            course_condition=self.race_info_normalizer.normalize_course_condition(
                race_info.course_run_info),
            race_start_time=self.race_info_normalizer.normalize_race_start_time(
                race_info.course_run_info),
            held_date=self.race_info_normalizer.normalize_held_date(
                race_info.held_date),
            held_place=SHUTUBA_RACE_INFO["place"],
            held_number=SHUTUBA_RACE_INFO["kaisu"],
            held_date_number=SHUTUBA_RACE_INFO["nichime"],
            explanation=self.race_info_normalizer.normalize_explanation(
                race_info.held_info)
        )

    def shape_race_detail_info(self, race_detail_info: RaceDetailInfo):
        return ShapedRaceDetailInfo(
            box_numbers=self.race_details_normalizer.normalize_box_numbers(
                race_detail_info.box_numbers),
            horse_numbers=self.race_details_normalizer.normalize_horse_numbers(
                race_detail_info.horse_numbers),
            horse_names=self.race_details_normalizer.normalize_horse_names(
                race_detail_info.horse_info),
            horse_ids=self.race_details_normalizer.normalize_horse_ids(
                race_detail_info.horse_ids),
            horse_sexes=self.race_details_normalizer.normalize_horse_sexes(
                race_detail_info.horse_ages_and_sexes),
            horse_ages=self.race_details_normalizer.normalize_horse_ages(
                race_detail_info.horse_ages_and_sexes),
            jockey_weights=self.race_details_normalizer.normalize_jockey_weights(
                race_detail_info.jockey_weights),
            jockey_names=self.race_details_normalizer.normalize_jockey_names(
                race_detail_info.jockey_names),
            # odds=self.race_details_normalizer.normalize_odds(
            #     race_detail_info.odds),
            popularities=self.race_details_normalizer.normalize_popularities(
                race_detail_info.popularities),
            horse_weights=self.race_details_normalizer.normalize_horse_weights(
                race_detail_info.horse_weights),
            horse_weight_diffs=self.race_details_normalizer.normalize_horse_weight_diffs(
                race_detail_info.horse_weights),
            trainer_names=self.race_details_normalizer.normalize_trainer_names(
                race_detail_info.trainer_names),
        )
