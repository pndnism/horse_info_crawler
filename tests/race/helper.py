from horse_info_crawler.race.domain import RaceDetailInfo, RaceInfo, ShapedRaceData, ShapedRaceDetailInfo, ShapedRaceInfo
import pandas as pd

def create_race_info(i: int):
    return RaceInfo (
        race_url=f"test_url_{i}",
        name=f"test_name_{i}",
        race_number=f"test_race_number_{i}",
        course_run_info=f"test_course_run_info_{i}",
        held_info=f"test_held_info_{i}",
        race_detail_info=RaceDetailInfo(
            arrival_orders=[f'test_arrival_orders_{i}'],
            box_numbers=[f'test_box_numbers_{i}'],
            horse_numbers=[f'test_horse_numbers_{i}'],
            horse_info=[f'test_horse_info_{i}'],
            horse_ages_and_sexes=[f'test_horse_ages_and_sexes_{i}'],
            jockey_weights=[f'test_jockey_weights_{i}'],
            jockey_names=[f'test_jockey_names_{i}'],
            goal_times=[f'test_goal_times_{i}'],
            goal_margins=[f'test_goal_margins_{i}'],
            order_transitions=[f'test_order_transitions_{i}'],
            half_times=[f'test_half_times_{i}'],
            odds=[f'test_odds_{i}'],
            popularities=[f'test_popularities_{i}'],
            horse_weights=[f'test_horse_weights_{i}'],
            trainer_names=[f'test_trainer_names_{i}'],
            horse_owners=[f'test_horse_owners_{i}'],
            earn_prizes=[f'test_earn_prizes_{i}'],
        )
    )

def create_shaped_race_data(i: int):
    return ShapedRaceData (
        ShapedRaceInfo(
            race_url=f"test_shaped_url_{i}",
            name=f'test_shaped_name_{i}',
            race_number=f'test_shaped_race_number_{i}',
            course_type=f'test_shaped_course_type_{i}',
            course_direction=f'test_shaped_course_direction_{i}',
            course_length=f'test_shaped_course_length_{i}',
            weather=f'test_shaped_weather_{i}',
            course_condition=f'test_shaped_course_condition_{i}',
            race_start_time=f'test_shaped_race_start_time_{i}',
            held_date=f'test_shaped_held_date_{i}',
            held_place=f'test_shaped_held_place_{i}',
            held_number=f'test_shaped_held_number_{i}',
            held_date_number=f'test_shaped_held_date_number_{i}',
            explanation=f'test_shaped_explanation_{i}',
        ),
        ShapedRaceDetailInfo(
            arrival_orders=[f'test_shaped_arrival_orders_{i}'],
            box_numbers=[f'test_shaped_box_numbers_{i}'],
            horse_numbers=[f'test_shaped_horse_numbers_{i}'],
            horse_names=[f'test_shaped_horse_names_{i}'],
            horse_ids=[f'test_shaped_horse_ids_{i}'],
            horse_sexes=[f'test_shaped_horse_sexes_{i}'],
            horse_ages=[f'test_shaped_horse_ages_{i}'],
            jockey_weights=[f'test_shaped_jockey_weights_{i}'],
            jockey_names=[f'test_shaped_jockey_names_{i}'],
            goal_times=[f'test_shaped_goal_times_{i}'],
            goal_margins=[f'test_shaped_goal_margins_{i}'],
            order_transitions=[f'test_shaped_order_transitions_{i}'],
            half_times=[f'test_shaped_half_times_{i}'],
            odds=[f'test_shaped_odds_{i}'],
            popularities=[f'test_shaped_popularities_{i}'],
            horse_weights=[f'test_shaped_horse_weights_{i}'],
            horse_weight_diffs=[f'test_shaped_horse_weight_diffs_{i}'],
            trainer_names=[f'test_shaped_trainer_names_{i}'],
            horse_owners=[f'test_shaped_horse_owners_{i}'],
            earn_prizes=[f'test_shaped_earn_prizes_{i}'],
        )
    )