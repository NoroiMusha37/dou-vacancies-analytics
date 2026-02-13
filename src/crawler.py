import logging
from datetime import datetime
from pathlib import Path

from scrapy.crawler import CrawlerProcess

from src.config import MainConfig
from src.scrape.spiders.python_vacancies_spider import PythonVacanciesSpider

SPIDERS = {
    "python": PythonVacanciesSpider,
}

logger = logging.getLogger(__name__)


def get_output_path(field: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = MainConfig.DATA_DIR / field / timestamp
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / MainConfig.CSV_NAME


def get_crawler_settings(output_path: Path) -> dict:
    settings = MainConfig.CRAWLER_SETTINGS.copy()
    settings["FEEDS"] = {
        str(output_path): {
            "format": "csv",
            "encoding": "utf-8",
            "overwrite": True,
        }
    }

    return settings


def run_spider(spider_key: str):
    spider_class = SPIDERS.get(spider_key)
    if not spider_class:
        logger.error(f"Spider {spider_key} is not supported")
        raise ValueError(f"Spider {spider_key} not supported")

    output_path = get_output_path(spider_key)

    settings = get_crawler_settings(output_path)

    logger.info(f"Starting spider for {spider_key} vacancies. Saving to {output_path}")

    process = CrawlerProcess(settings=settings)
    process.crawl(spider_class)
    process.start()
