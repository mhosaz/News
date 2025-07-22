import requests

class ZoomitScraperPipeline:
    def process_item(self, item, spider):
        payload = {
            "title": item.get("title"),
            "content": item.get("content"),
            "source": item.get("source"),
            "tags": item.get("tags", [])
        }

        spider.logger.warning(f"Posting item: {payload}")

        response = requests.post("http://127.0.0.1:8000/news/news/", json=payload)

        spider.logger.warning(f"Response: {response.status_code} | {response.text}")
        return item
