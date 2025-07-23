import os
import sys

# Add the project root to sys.path (2 levels up from this file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from zoomit_scraper.zoomit_scraper.spiders.news_spider import ZoomitNewsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZoomitNewsSpider)
    process.start()

if __name__ == "__main__":
    run()
