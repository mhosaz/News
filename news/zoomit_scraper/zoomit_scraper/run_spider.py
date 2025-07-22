from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zoomit_scraper.spiders.news_spider import ZoomitNewsSpider

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZoomitNewsSpider)
    process.start()
