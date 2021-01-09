from horse_info_crawler.race.domain import RaceInfo

def create_race_info(i: int):
    return RaceInfo (
        name=f"test_name_{i}",
        address=f"test_address_{i}",
        completed_on=f"test_completed_on_{i}",
        earthquake_resistance=f"test_earthquake_resistance_{i}",
        standard_floor_area=f"test_standard_floor_area_{i}",
        appearance_img_url=f"test_appearance_img_url_{i}",
        layout_img_url=f"test_layout_img_url_{i}",
        building_use=f"test_building_use_{i}",
        detail_link=f"test_detail_link_{i}",
        agent_building_code=f"test_agent_building_code_{i}",
    )