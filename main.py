from typing import Optional
import click
from horse_info_crawler.race import usecases as race_usecases
import sentry_sdk


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
    click.echo(f"crawl_race_info Started. crawl_limit:{crawl_limit}")
    usecase = race_usecases.get_crawl_race_histories_usecase()
    usecase.exec(crawl_limit)

    click.echo("crawl_race_history Completed")

if __name__ == '__main__':
    sentry_sdk.init(
    "https://317bab5f08b64718afadc66afe0a0cce@o495078.ingest.sentry.io/5567225",
    traces_sample_rate=1.0
    )
    main()
    