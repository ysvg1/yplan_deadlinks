import scrapy
import requests
import logging
from datetime import datetime

YPLAN_BASE_URL = 'yplanapp.com'

logging.basicConfig(
    filename='log_deadlinks_%s.txt' % datetime.now().replace(microsecond=0).isoformat()
)

class DeadlinkSpider(scrapy.Spider):
    name = 'deadlink_finder'

    def __init__(self, list_all_links=False, max_pages=0, *args, **kwargs):
        super(DeadlinkSpider, self).__init__(*args, **kwargs)

        self.max_pages = int(max_pages)
        logging.info("Limit on folliwing website's internal links: %d" % self.max_pages)

        self.list_all_links = bool(list_all_links)
        logging.info("List all encountered valid HTTP/HTTPS links, not only broken ones: %s" % self.list_all_links)
        self.followed_links_count = 0


    def start_requests(self):
        urls = [
            'https://' + YPLAN_BASE_URL,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        link_hrefs = response.css('a::attr(href)').extract()
        for link in link_hrefs:
            link = str(link).strip()
            if ':' in link and link.split(':')[0] not in ["http", "https"]:
                logging.debug("non-http scheme: %s\n\n" % link)
                continue

            try:
                if link.startswith('/') or link.startswith('?') or link.startswith(YPLAN_BASE_URL):
                    if self.followed_links_count < self.max_pages or self.max_pages <= 0:
                        self.followed_links_count += 1
                        yield scrapy.Request(url='https://' + YPLAN_BASE_URL + link, callback=self.parse)
                else:
                    try:
                        head_response = requests.head(url=link, timeout=10)
                        if head_response.status_code < 200 or head_response.status_code >= 400:
                            yield {'url': link, 'is_broken': 1, 'info': head_response.status_code}
                        elif self.list_all_links:
                            yield {'url': link, 'is_broken': 0, 'info': ''}

                    except requests.exceptions.RequestException as exc:
                        yield {
                            'url': link,
                            'is_broken': 1,
                            'info': str(exc)
                        }
            except Exception as generic_exc:
                logging.error(generic_exc)
