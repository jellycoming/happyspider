# coding=utf-8
import os
import sys
import json
import logging
from happyspider.utils import find_class

logger = logging.getLogger(__name__)


class Transporter(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self._drivers = self.project.settings.TRANSPORTER_DRIVERS
        super(Transporter, self).__init__()

    def run(self):
        while True:
            spider, item = self.scheduler.get_task(self)
            self._transport(spider, item)

    def _transport(self, spider, item):
        for d in self._drivers:
            driver = find_class(d)()
            logger.debug('{} thread safety: {}'.format(driver.__class__, driver.thread_safety))
            if driver.thread_safety:
                self.scheduler.acquire_lock()
                try:
                    driver.transport(spider, item)
                except Exception:
                    raise
                finally:
                    self.scheduler.release_lock()
            else:
                driver.transport(spider, item)

    @property
    def project(self):
        return self.scheduler.project


class Driver(object):
    def __init__(self, thread_safety=False):
        self.thread_safety = thread_safety
        super(Driver, self).__init__()

    def transport(self, spider, item):
        raise NotImplementedError


class ConsoleDriver(Driver):
    def __init__(self):
        super(ConsoleDriver, self).__init__()

    def transport(self, spider, item):
        sys.stdout.write(json.dumps(item, indent=4, ensure_ascii=False))
        sys.stdout.write(os.linesep)