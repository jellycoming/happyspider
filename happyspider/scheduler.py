# coding=utf-8
import logging
import time
import traceback
from threading import Lock, Semaphore
from happyspider.types import Request, Response, Item
from happyspider.spiderloader import SpiderLoader
from happyspider.utils import run_in_thread
from happyspider.crawler import Crawler, PhantomJSDriver
from happyspider.parser import Parser
from happyspider.transporter import Transporter

logger = logging.getLogger(__name__)


class Scheduler(object):
    def __init__(self, project, request_queue, response_queue, item_queue):
        logger.debug('初始化调度器')
        self._project = project
        self._request_queue = request_queue
        self._response_queue = response_queue
        self._item_queue = item_queue
        self._spider_loader = SpiderLoader(project=self._project)
        self._quit = False
        self._wait_times = 0
        self._lock = Lock()
        self._semaphore = Semaphore(self.settings.PHANTOMJS_PROC)
        self.phantomjs_drivers = []
        self.phantomjs_drivers_invoked = False

    def run(self):
        logger.debug('启动调度器')
        while not self._quit:
            try:
                self.invoke_crawler()
                self.invoke_parser()
                self.invoke_transporter()
                self.invoke_phantomjs_drivers()
                self._invoke_all_spiders()
                self._wait_loop()
            except KeyboardInterrupt:
                break
            except Exception:
                logger.error('调度器异常: \n' + traceback.format_exc())
                break
        self.clear_phantomjs_drivers()
        logger.debug('调度器退出')

    def list(self):
        return self._spider_loader.list()

    def invoke_crawler(self):
        logger.debug('启动Crawler组件,线程数: ' + str(self.settings.CRAWLER_NUM))
        for _ in range(self.settings.CRAWLER_NUM):
            run_in_thread(Crawler(self).run)

    def invoke_parser(self):
        logger.debug('启动Parser组件,线程数: ' + str(self.settings.PARSER_NUM))
        for _ in range(self.settings.PARSER_NUM):
            run_in_thread(Parser(self).run)

    def invoke_transporter(self):
        logger.debug('启动Transporter组件, 线程数: ' + str(self.settings.TRANSPORTER_NUM))
        for _ in range(self.settings.TRANSPORTER_NUM):
            run_in_thread(Transporter(self).run)

    def invoke_phantomjs_drivers(self):
        if self.settings.PHANTOMJS_SETTING:
            logger.debug('启动Phantomjs Driver进程, 进程数: ' + str(self.settings.PHANTOMJS_PROC))
            for _ in range(self.settings.PHANTOMJS_PROC):
                self.phantomjs_drivers.append(PhantomJSDriver(**self.settings.PHANTOMJS_SETTING))
            self.phantomjs_drivers_invoked = True

    def clear_phantomjs_drivers(self):
        if self.phantomjs_drivers_invoked:
            logger.debug('清理Phantomjs Driver进程组')
            for driver in self.phantomjs_drivers:
                driver.quit()
            self.phantomjs_drivers_invoked = False

    def new_task(self, spider, task):
        _task_queue = self._task_queue(type(task))
        _task_queue.put((spider, task))

    def get_task(self, who):
        _task_queue = self._task_queue(type(who))
        return _task_queue.get()

    def stat(self):
        return 'request_queue: {}, response_queue: {}, item_queue: {}'\
            .format(self._request_queue.qsize(), self._response_queue.qsize(), self._item_queue.qsize())

    def _invoke_all_spiders(self):
        _waiting = self._project.waiting or self._spider_loader.list()
        logger.debug('启动爬虫队列: ' + str(_waiting))
        spiderclses = [self._spider_loader.load(spider_name) for spider_name in _waiting]
        for spidercls in spiderclses:
            self._invoke_spider(spidercls)

    def _invoke_spider(self, spidercls):
        spider = spidercls()
        for obj in getattr(spider, 'start')():
            self.new_task(spider, obj)

    def _task_queue(self, _type):
        if _type in (Transporter, Item):
            return self._item_queue
        elif _type in (Crawler, Request):
            return self._request_queue
        elif _type in (Parser, Response):
            return self._response_queue
        else:
            raise TypeError('Unsupported type {}.'.format(_type))

    def _wait_loop(self):
        while True:
            if all(queue.empty() for queue in (self._request_queue, self._response_queue, self._item_queue)) \
                    and (not self._phantomjs_driver_running()):
                self._wait_times += 1
                if self._wait_times > self.settings.SCHEDULER_WAIT_TIMES:
                    break
                time.sleep(self.settings.SCHEDULER_WAIT_SECS)
        self._quit = True

    def _phantomjs_driver_running(self):
        return self.phantomjs_drivers_invoked and (not len(self.phantomjs_drivers) == self.settings.PHANTOMJS_PROC)

    @property
    def project(self):
        return self._project

    @property
    def settings(self):
        return self._project.settings

    def acquire_lock(self):
        self._lock.acquire()

    def release_lock(self):
        self._lock.release()

    def wait_lock(self, timeout=None):
        self._lock.wait(timeout=timeout)

    def acquire_semaphore(self):
        self._semaphore.acquire()

    def release_semaphore(self):
        self._semaphore.release()

