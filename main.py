from typing import Optional
import click
from horse_info_crawler.race import usecases as race_usecases


@click.group()
def main():
    pass

@main.command("race")
@click.option("--crawl-limit", default=None, type=int)
def crawl_race_history(crawl_limit: Optional[int]):
    """Crawl race history.
    Args:
        crawl_limit Optional[int]: the max number of properties to crawl.
    """
    click.echo(f"crawl_cbre_properties Started. crawl_limit:{crawl_limit}")
    usecase = race_usecases.get_crawl_race_histories_usecase()
    usecase.exec(crawl_limit)

    click.echo("crawl_cbre_properties Completed")

if __name__ == '__main__':
    main()