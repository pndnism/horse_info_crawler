from horse_info_crawler.race.domain import RaceInfo
import pandas as pd

def create_race_info(i: int):
    return RaceInfo (
        name=f"test_name_{i}",
        race_number=f"test_race_number_{i}",
        course_run_info=f"test_course_run_info_{i}",
        held_info=f"test_held_info_{i}",
        race_details=pd.DataFrame()
    )