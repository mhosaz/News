import subprocess
from celery import shared_task

@shared_task
def run_scraper():
    subprocess.run(['python', 'zoomit_scraper/run_spider.py'])
