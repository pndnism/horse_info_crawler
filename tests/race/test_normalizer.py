from horse_info_crawler.race.normalizer import InvalidFormatError, RaceInfoNormalizer
from unittest import TestCase


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