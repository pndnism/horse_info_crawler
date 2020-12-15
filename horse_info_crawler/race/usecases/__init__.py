from datetime import datetime
from horse_info_crawler.race.normalizer import RaceDetailsNormalizer, RaceInfoNormalizer
from horse_info_crawler.race.shaper import RaceInfoShaper
from horse_info_crawler.race.repository import DataFormatter, RaceInfoRepository
from horse_info_crawler.race.parser import RaceInfoListingPageParser, RaceInfoParser
from horse_info_crawler.race.scraper import RaceInfoListingPageScraper, RaceInfoScraper
from horse_info_crawler.race.usecases.crawl_all_race_histories import CrawlRaceHistoriesUsecase




def get_crawl_race_histories_usecase() -> CrawlRaceHistoriesUsecase:
    return CrawlRaceHistoriesUsecase(
        race_info_listing_page_scraper=RaceInfoListingPageScraper(
            parser=RaceInfoListingPageParser(),
        ),
        race_info_scraper=RaceInfoScraper(
            parser=RaceInfoParser(),
        ),
        race_info_repository=RaceInfoRepository(
            formatter=DataFormatter(),
            current_datetime=datetime.now()
        ),
        race_info_shaper=RaceInfoShaper(
            race_info_normalizer=RaceInfoNormalizer(),
            race_details_normalizer=RaceDetailsNormalizer()
        )
    )