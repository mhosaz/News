import scrapy
import re

class ZoomitNewsSpider(scrapy.Spider):
    name = "zoomit_news"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/"]

    def parse(self, response):
        article_links = response.css("div.flex-col.flex.gap-4.px-4 a::attr(href)").getall()
        for link in article_links:
            print("\n\n\n\n\n==============")
            print(link)
            print("=============\n\n\n\n\n\n")
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        # Extract title
        print(response.url)
        title = response.css("h1::text").get()
        print(title)
        # Extract content (all <p> inside the article)
        paragraphs = response.css("article p::text").getall()
        content = " ".join([p.strip() for p in paragraphs if p.strip()])
        content = re.sub(r"\s+", " ", content)
        # Extract tags
        h1 = response.css("h1")  # Keep as Selector (don't use .get())
        tags = h1.xpath('''
            ./following-sibling::div[
                .//span[contains(@class, "sc-9996cfc-0") and contains(@class, "NawFH")]
            ]//span[contains(@class, "sc-9996cfc-0")]/text()
        ''').getall()
        tags = tags[:-2]
        print("\n\n\n\n\n==============")
        print(tags)
        print("=============\n\n\n\n\n\n")
        yield {
            "title": title,
            "content": content,
            "source": response.url,
            "tags": tags
        }

