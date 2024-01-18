import scrapy


class WorkUaSpider(scrapy.Spider):
    name = "workua"
    start_urls = ["https://www.work.ua/jobs-remote-python/"]
