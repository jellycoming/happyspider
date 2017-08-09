# coding=utf-8
from happyspider.types import Request


class Spider(object):
    name = ''
    start_urls = []

    def start(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url=url, callback=self.parse, headers=getattr(self, 'headers', None))

    def parse(self, response):
        raise NotImplementedError
