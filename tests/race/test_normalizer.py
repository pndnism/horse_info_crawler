from horse_info_crawler.race.normalizer import RaceInfoNormalizer
from unittest import TestCase

class TestRaceInfoNormalizer(TestCase):

    def test_normalize_name(self):
        self.assertEqual(RaceInfoNormalizer.normalize_name('第39回ジャパンカップ(G1)','第39回ジャパンカップ(G1)'))

    def test_normalize_race_number(self):
        self.assertEqual(RaceInfoNormalizer.normalize_name('11 R','11'))