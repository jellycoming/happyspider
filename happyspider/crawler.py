# coding=utf-8
import threading
import logging
import requests
from selenium import webdriver
from happyspider.types import Response

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Crawler(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler
        super(Crawler, self).__init__()

    def run(self):
        while True:
            spider, request = self.scheduler.get_task(self)
            try:
                response = self._crawl(request)
                logger.debug('{} [SUCCEED]'.format(request.url))
                self.scheduler.new_task(spider, response)
            except Exception as e:
                logger.debug('{} [FAILED]: {}'.format(request.url, str(e)))
                raise

    def _crawl(self, request):
        driver_name = request.driver or Driver.REQUESTS
        if driver_name == Driver.PHANTOMJS:
            assert self.scheduler.phantomjs_drivers_invoked, 'Can not use phantomjs drivers, please invoke first'
            self.scheduler.acquire_semaphore()
            driver = self.scheduler.phantomjs_drivers.pop()
            try:
                response = driver.fetch(request)
            except Exception:
                raise
            finally:
                self.scheduler.phantomjs_drivers.append(driver)
                self.scheduler.release_semaphore()
        else:
            response = RequestsDriver().fetch(request)
        return response


class Driver(object):
    PHANTOMJS = 'phantomjs'
    REQUESTS = 'requests'

    def fetch(self, request):
        raise NotImplementedError


class PhantomJSDriver(Driver):
    def __init__(self, **kwargs):
        self._driver = webdriver.PhantomJS(**kwargs)

    def fetch(self, request):
        self._driver.get(request.url)
        return Response(url=request.url, html=self._driver.page_source, callback=request.callback)

    def quit(self):
        self._driver.quit()


class RequestsDriver(Driver):
    def fetch(self, request):
        res = requests.request(method=request.method, url=request.url, params=request.params, data=request.data,
                               headers=request.headers, cookies=request.cookies, verify=True)
        return Response(url=request.url, html=res.text, callback=request.callback)