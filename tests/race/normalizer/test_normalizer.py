import os
from tests.race.normalizer.data.test_race_detail_lists import NORMALIZED_ARRIVAL_ORDERS_LIST, NORMALIZED_BOX_NUMBERS_LIST, NORMALIZED_EARN_PRIZES_LIST, NORMALIZED_GOAL_MARGINS_LIST, NORMALIZED_GOAL_TIMES_LIST, NORMALIZED_HALF_TIMES_LIST, NORMALIZED_HORSE_AGES_LIST, NORMALIZED_HORSE_NAMES_LIST, NORMALIZED_HORSE_NUMBERS_LIST, NORMALIZED_HORSE_OWNERS_LIST, NORMALIZED_HORSE_SEXES_LIST, NORMALIZED_HORSE_WEIGHTS_LIST, NORMALIZED_HORSE_WEIGHT_DIFFS_LIST, NORMALIZED_JOCKEY_NAMES_LIST, NORMALIZED_JOCKEY_WEIGHTS_LIST, NORMALIZED_ODDS_LIST, NORMALIZED_ORDER_TRANSITIONS_LIST, NORMALIZED_POPULARITIES_LIST, NORMALIZED_TRAINER_NAMES_LIST
from horse_info_crawler.race.normalizer import InvalidFormatError, RaceDetailsNormalizer, RaceInfoNormalizer
from unittest import TestCase
import pandas as pd


class TestRaceInfoNormalizer(TestCase):

    def test_normalize_name(self):
        self.assertEqual(RaceInfoNormalizer.normalize_name(
            '第39回ジャパンカップ(G1)'), '第39回ジャパンカップ(G1)')

    def test_normalize_race_number(self):
        self.assertEqual(
            RaceInfoNormalizer.normalize_race_number('11 R'), '11')

    def test_normalize_course_type(self):
        self.assertEqual(RaceInfoNormalizer.normalize_course_type(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '芝')

    def test_normalize_course_direction(self):
        self.assertEqual(RaceInfoNormalizer.normalize_course_direction(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '左')

    def test_normalize_course_length(self):
        self.assertEqual(RaceInfoNormalizer.normalize_course_length(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '2400')

    def test_normalize_weather(self):
        self.assertEqual(RaceInfoNormalizer.normalize_weather(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '曇')

        with self.assertRaises(InvalidFormatError):
                RaceInfoNormalizer.normalize_weather('invalid data')

    def test_normalize_course_condition(self):
        self.assertEqual(RaceInfoNormalizer.normalize_course_condition(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '重')

    def test_normalize_race_start_time(self):
        self.assertEqual(RaceInfoNormalizer.normalize_race_start_time(
            '芝左2400m / 天候 : 曇 / 芝 : 重 / 発走 : 15:40'), '15:40')

    def test_normalize_held_date(self):
        self.assertEqual(RaceInfoNormalizer.normalize_held_date(
            '2019年11月24日 5回東京8日目 3歳以上オープン  (国際)(指)(定量)'), '2019年11月24日')

    def test_normalize_held_place(self):
        self.assertEqual(RaceInfoNormalizer.normalize_held_place(
            '2019年11月24日 5回東京8日目 3歳以上オープン  (国際)(指)(定量)'), '東京')

    def test_normalize_held_number(self):
        self.assertEqual(RaceInfoNormalizer.normalize_held_number(
            '2019年11月24日 5回東京8日目 3歳以上オープン  (国際)(指)(定量)'), '5')

    def test_normalize_held_date_number(self):
        self.assertEqual(RaceInfoNormalizer.normalize_held_date_number(
            '2019年11月24日 5回東京8日目 3歳以上オープン  (国際)(指)(定量)'), '8')

    def test_normalize_explanation(self):
        self.assertEqual(RaceInfoNormalizer.normalize_explanation(
            '2019年11月24日 5回東京8日目 3歳以上オープン  (国際)(指)(定量)'), '3歳以上オープン(国際)(指)(定量)')

class TestRaceDetailsNormalizer(TestCase):
    source_df = pd.read_pickle(
                f"{os.path.dirname(__file__)}/data/test_race_info_dataframe.pkl")

    def test_normalize_arrival_orders(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_arrival_orders(self.source_df), NORMALIZED_ARRIVAL_ORDERS_LIST)

    def test_normalize_box_numbers(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_box_numbers(self.source_df), NORMALIZED_BOX_NUMBERS_LIST)

    def test_normalize_horse_numbers(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_numbers(self.source_df), NORMALIZED_HORSE_NUMBERS_LIST)

    def test_normalize_horse_names(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_names(self.source_df), NORMALIZED_HORSE_NAMES_LIST)

    def test_normalize_horse_sexes(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_sexes(self.source_df), NORMALIZED_HORSE_SEXES_LIST)

    def test_normalize_horse_ages(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_ages(self.source_df), NORMALIZED_HORSE_AGES_LIST)

    def test_normalize_jockey_weights(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_jockey_weights(self.source_df), NORMALIZED_JOCKEY_WEIGHTS_LIST)

    def test_normalize_jockey_names(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_jockey_names(self.source_df), NORMALIZED_JOCKEY_NAMES_LIST)

    def test_normalize_goal_times(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_goal_times(self.source_df), NORMALIZED_GOAL_TIMES_LIST)

    def test_normalize_goal_margins(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_goal_margins(self.source_df), NORMALIZED_GOAL_MARGINS_LIST)

    def test_normalize_order_transitions(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_order_transitions(self.source_df), NORMALIZED_ORDER_TRANSITIONS_LIST)

    def test_normalize_half_times(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_half_times(self.source_df), NORMALIZED_HALF_TIMES_LIST)

    def test_normalize_odds(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_odds(self.source_df), NORMALIZED_ODDS_LIST)

    def test_normalize_popularities(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_popularities(self.source_df), NORMALIZED_POPULARITIES_LIST)

    def test_normalize_horse_weights(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_weights(self.source_df), NORMALIZED_HORSE_WEIGHTS_LIST)
    
    def test_normalize_horse_weight_diffs(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_weight_diffs(self.source_df), NORMALIZED_HORSE_WEIGHT_DIFFS_LIST)

    def test_normalize_trainer_names(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_trainer_names(self.source_df), NORMALIZED_TRAINER_NAMES_LIST)

    def test_normalize_horse_owners(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_horse_owners(self.source_df), NORMALIZED_HORSE_OWNERS_LIST)
    
    def test_normalize_earn_prizes(self):
        self.assertEqual(RaceDetailsNormalizer.normalize_earn_prizes(self.source_df), NORMALIZED_EARN_PRIZES_LIST)