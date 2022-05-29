from datetime import datetime
from horse_info_crawler.shutsuba_info.normalizer import RaceDetailsNormalizer, RaceInfoNormalizer
from horse_info_crawler.shutsuba_info.shaper import RaceInfoShaper
from horse_info_crawler.shutsuba_info.repository import DataFormatter, RaceInfoRepository
from horse_info_crawler.shutsuba_info.parser import RaceInfoParser
from horse_info_crawler.shutsuba_info.scraper import RaceInfoScraper
from horse_info_crawler.shutsuba_info.usecases.crawl_shutsuba_hyou import CrawlShutsubaHyouUsecase


def get_crawl_shutsuba_info_usecase() -> CrawlShutsubaHyouUsecase:
    return CrawlShutsubaHyouUsecase(
        # race_info_listing_page_scraper=RaceInfoListingPageScraper(
        #     parser=RaceInfoListingPageParser(),
        # ),
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
