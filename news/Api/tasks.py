import subprocess
import sys
from celery import shared_task
import os

@shared_task
def run_zoomit_spider():
    venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')  # Windows path
    subprocess.run([venv_python, "zoomit_scraper/zoomit_scraper/run_spider.py"], check=True)
