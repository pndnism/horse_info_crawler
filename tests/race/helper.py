from horse_info_crawler.race.domain import RaceInfo, ShapedRaceData, ShapedRaceDetailInfo, ShapedRaceInfo
import pandas as pd

def create_race_info(i: int):
    return RaceInfo (
        name=f"test_name_{i}",
        race_number=f"test_race_number_{i}",
        course_run_info=f"test_course_run_info_{i}",
        held_info=f"test_held_info_{i}",
        race_details=pd.DataFrame({"x":[1,1,1,1]})
    )

def create_shaped_race_data(i: int):
    return ShapedRaceData (
        ShapedRaceInfo(
            name=f'test_name_{i}',
            race_number=f'test_race_number_{i}',
            course_type=f'test_course_type_{i}',
            course_direction=f'test_course_direction_{i}',
            course_length=f'test_course_length_{i}',
            weather=f'test_weather_{i}',
            course_condition=f'test_course_condition_{i}',
            race_start_time=f'test_race_start_time_{i}',
            held_date=f'test_held_date_{i}',
            held_place=f'test_held_place_{i}',
            held_number=f'test_held_number_{i}',
            held_date_number=f'test_held_date_number_{i}',
            explanation=f'test_explanation_{i}',
        ),
        ShapedRaceDetailInfo(
            arrival_orders=[f'test_arrival_orders_{i}'],
            box_numbers=[f'test_box_numbers_{i}'],
            horse_numbers=[f'test_horse_numbers_{i}'],
            horse_names=[f'test_horse_names_{i}'],
            horse_sexes=[f'test_horse_sexes_{i}'],
            horse_ages=[f'test_horse_ages_{i}'],
            jockey_weights=[f'test_jockey_weights_{i}'],
            jockey_names=[f'test_jockey_names_{i}'],
            goal_times=[f'test_goal_times_{i}'],
            goal_margins=[f'test_goal_margins_{i}'],
            order_transitions=[f'test_order_transitions_{i}'],
            half_times=[f'test_half_times_{i}'],
            odds=[f'test_odds_{i}'],
            popularities=[f'test_popularities_{i}'],
            horse_weights=[f'test_horse_weights_{i}'],
            horse_weight_diffs=[f'test_horse_weight_diffs_{i}'],
            trainer_names=[f'test_trainer_names_{i}'],
            horse_owners=[f'test_horse_owners_{i}'],
            earn_prizes=[f'test_earn_prizes_{i}'],
        )
    )