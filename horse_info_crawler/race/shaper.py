from dataclasses import dataclass
from horse_info_crawler.race.normalizer import RaceDetailsNormalizer, RaceInfoNormalizer
from horse_info_crawler.race.domain import RaceInfo, ShapedRaceData, ShapedRaceDetailInfo, ShapedRaceInfo
from typing import Type

@dataclass
class RaceInfoShaper:
    race_info_normalizer: Type[RaceInfoNormalizer]
    race_details_normalizer: Type[RaceDetailsNormalizer]

    def shape(self, race_info: RaceInfo) -> ShapedRaceData:
        return ShapedRaceData(
            shaped_race_info=self.shape_race_info(race_info),
            shaped_race_detail_info=self.shape_race_detail_info(race_info)
        )

    def shape_race_info(self, race_info: RaceInfo):
        return ShapedRaceInfo(
            name = self.race_info_normalizer.normalize_name(race_info.name),
            race_number = self.race_info_normalizer.normalize_race_number(race_info.race_number),
            course_type = self.race_info_normalizer.normalize_course_type(race_info.course_run_info),
            course_direction = self.race_info_normalizer.normalize_course_direction(race_info.course_run_info),
            course_length = self.race_info_normalizer.normalize_course_length(race_info.course_run_info),
            weather = self.race_info_normalizer.normalize_weather(race_info.course_run_info),
            course_condition = self.race_info_normalizer.normalize_course_condition(race_info.course_run_info),
            race_start_time = self.race_info_normalizer.normalize_race_start_time(race_info.course_run_info),
            held_date = self.race_info_normalizer.normalize_held_date(race_info.held_info),
            held_place = self.race_info_normalizer.normalize_held_place(race_info.held_info),
            held_number = self.race_info_normalizer.normalize_held_number(race_info.held_info),
            held_date_number = self.race_info_normalizer.normalize_held_date_number(race_info.held_info),
            explanation = self.race_info_normalizer.normalize_explanation(race_info.held_info),
            race_details = self.race_info_normalizer.normalize_race_details(race_info.race_details),
        )

    def shape_race_detail_info(self, race_info: RaceInfo):
        return ShapedRaceDetailInfo(
            arrival_orders = self.race_details_normalizer.normalize_arrival_orders(race_info.race_details),
            box_numbers = self.race_details_normalizer.normalize_box_numbers(race_info.race_details),
            horse_numbers = self.race_details_normalizer.normalize_horse_numbers(race_info.race_details),
            horse_names = self.race_details_normalizer.normalize_horse_names(race_info.race_details),
            horse_sexes = self.race_details_normalizer.normalize_horse_sexes(race_info.race_details),
            horse_ages = self.race_details_normalizer.normalize_horse_ages(race_info.race_details),
            jockey_weights = self.race_details_normalizer.normalize_jockey_weights(race_info.race_details),
            jockey_names = self.race_details_normalizer.normalize_jockey_names(race_info.race_details),
            goal_times = self.race_details_normalizer.normalize_goal_times(race_info.race_details),
            goal_margins = self.race_details_normalizer.normalize_goal_margins(race_info.race_details),
            order_transitions = self.race_details_normalizer.normalize_order_transitions(race_info.race_details),
            half_times = self.race_details_normalizer.normalize_half_times(race_info.race_details),
            odds = self.race_details_normalizer.normalize_odds(race_info.race_details),
            popularities = self.race_details_normalizer.normalize_popularities(race_info.race_details),
            horse_weights = self.race_details_normalizer.normalize_horse_weights(race_info.race_details),
            horse_weight_diffs = self.race_details_normalizer.normalize_horse_weight_diffs(race_info.race_details),
            trainer_names = self.race_details_normalizer.normalize_trainer_names(race_info.race_details),
            horse_owners = self.race_details_normalizer.normalize_horse_owners(race_info.race_details),
            earn_prizes = self.race_details_normalizer.normalize_earn_prizes(race_info.race_details),
        )