from datetime import datetime
from horse_info_crawler.pedigree.normalizer import HorseInfoNormalizer
from horse_info_crawler.pedigree.shaper import HorseInfoShaper
from horse_info_crawler.pedigree.repository import DataFormatter, HorseInfoRepository
from horse_info_crawler.pedigree.parser import HorseInfoListingPageParser, HorseInfoParser
from horse_info_crawler.pedigree.scraper import HorseInfoListingPageScraper, HorseInfoScraper
from horse_info_crawler.pedigree.usecases.crawl_all_horse_info import CrawlHorseInfoUsecase



def get_crawl_horse_info_usecase() -> CrawlHorseInfoUsecase:
    return CrawlHorseInfoUsecase(
        horse_info_listing_page_scraper=HorseInfoListingPageScraper(
            parser=HorseInfoListingPageParser(),
        ),
        horse_info_scraper=HorseInfoScraper(
            parser=HorseInfoParser(),
        ),
        horse_info_repository=HorseInfoRepository(
            formatter=DataFormatter(),
            current_datetime=datetime.now()
        ),
        horse_info_shaper=HorseInfoShaper(
            horse_info_normalizer=HorseInfoNormalizer()
        )
    )