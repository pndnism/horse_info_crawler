from dataclasses import dataclass
from horse_info_crawler.race.normalizer import RaceDetailsNormalizer, RaceInfoNormalizer
from horse_info_crawler.race.domain import RaceDetailInfo, RaceInfo, ShapedRaceData, ShapedRaceDetailInfo, ShapedRaceInfo
from typing import Type


@dataclass
class RaceInfoShaper:
    race_info_normalizer: Type[RaceInfoNormalizer]
    race_details_normalizer: Type[RaceDetailsNormalizer]

    def shape(self, race_info: RaceInfo) -> ShapedRaceData:
        return ShapedRaceData(
            shaped_race_info=self.shape_race_info(race_info),
            shaped_race_detail_info=self.shape_race_detail_info(race_info.race_detail_info)
        )

    def shape_race_info(self, race_info: RaceInfo):
        return ShapedRaceInfo(
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
                race_info.held_info),
            held_place=self.race_info_normalizer.normalize_held_place(
                race_info.held_info),
            held_number=self.race_info_normalizer.normalize_held_number(
                race_info.held_info),
            held_date_number=self.race_info_normalizer.normalize_held_date_number(
                race_info.held_info),
            explanation=self.race_info_normalizer.normalize_explanation(
                race_info.held_info)
                )

    def shape_race_detail_info(self, race_detail_info: RaceDetailInfo):
        return ShapedRaceDetailInfo(
            arrival_orders=self.race_details_normalizer.normalize_arrival_orders(
                race_detail_info.arrival_orders),
            box_numbers=self.race_details_normalizer.normalize_box_numbers(
                race_detail_info.box_numbers),
            horse_numbers=self.race_details_normalizer.normalize_horse_numbers(
                race_detail_info.horse_numbers),
            horse_names=self.race_details_normalizer.normalize_horse_names(
                race_detail_info.horse_info),
            horse_ids=self.race_details_normalizer.normalize_horse_ids(
                race_detail_info.horse_info),
            horse_sexes=self.race_details_normalizer.normalize_horse_sexes(
                race_detail_info.horse_ages_and_sexes),
            horse_ages=self.race_details_normalizer.normalize_horse_ages(
                race_detail_info.horse_ages_and_sexes),
            jockey_weights=self.race_details_normalizer.normalize_jockey_weights(
                race_detail_info.jockey_weights),
            jockey_names=self.race_details_normalizer.normalize_jockey_names(
                race_detail_info.jockey_names),
            goal_times=self.race_details_normalizer.normalize_goal_times(
                race_detail_info.goal_times),
            goal_margins=self.race_details_normalizer.normalize_goal_margins(
                race_detail_info.goal_margins),
            order_transitions=self.race_details_normalizer.normalize_order_transitions(
                race_detail_info.order_transitions),
            half_times=self.race_details_normalizer.normalize_half_times(
                race_detail_info.half_times),
            odds=self.race_details_normalizer.normalize_odds(
                race_detail_info.odds),
            popularities=self.race_details_normalizer.normalize_popularities(
                race_detail_info.popularities),
            horse_weights=self.race_details_normalizer.normalize_horse_weights(
                race_detail_info.horse_weights),
            horse_weight_diffs=self.race_details_normalizer.normalize_horse_weight_diffs(
                race_detail_info.horse_weights),
            trainer_names=self.race_details_normalizer.normalize_trainer_names(
                race_detail_info.trainer_names),
            horse_owners=self.race_details_normalizer.normalize_horse_owners(
                race_detail_info.horse_owners),
            earn_prizes=self.race_details_normalizer.normalize_earn_prizes(
                race_detail_info.earn_prizes),
        )
