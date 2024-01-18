import re

import scrapy


class WorkUaSpider(scrapy.Spider):
    name = "workua"
    start_urls = ["https://www.work.ua/jobs-remote-python/"]

def parse_vacancy(self, response):
    title = response.xpath('//h1[@id="h1-name"]/text()').get()

    salary = (
        response.css(".glyphicon-hryvnia")[-1]
            .xpath("./following-sibling::span/text()")
            .get()
            .replace("\u202f", "")
            .replace("\xa0", "")
            .replace("\u2009", "")
    )
    if "грн" not in salary:
        salary = None

    description = ("".join(response.xpath('//div[@id="job-description"]/p').getall())
                   .replace("<p>", "")
                   .replace("</p>", "")
                   .replace("<b>", " ")
                   .replace("</b>", " ")
                   )

    pattern = re.compile(r'<a\s+([^>]*\s+)?href\s*=\s*["\'](http[s]?://[^"\']*)["\'][^>]*>.*?</a>', flags=re.DOTALL)
    cleaned_description = pattern.sub('', description)

    employer = (
        response.css(".glyphicon-company").xpath("./following-sibling::a/span/text()").get()
    )

    yield {
        "url": response.url,
        "title": title,
        "salary": salary,
        "employer": employer,
        "description": cleaned_description,
    }


def parse(self, response):
    for card in response.css(".job-link"):
        vacancy_url = card.css(".add-bottom").xpath("./h2/a/@href").get()
        if vacancy_url is None:
            continue

        yield response.follow(vacancy_url, callback=self.parse_vacancy)

    next_page = response.css(".pagination li")[-1]
    if "disable" not in next_page.xpath("./@class").get():
        href = next_page.xpath("./a/@href").get()
        yield response.follow(href, callback=self.parse)
