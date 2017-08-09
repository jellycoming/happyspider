# coding=utf-8
import logging

logger = logging.getLogger(__name__)


class Parser(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler
        super(Parser, self).__init__()

    def run(self):
        while True:
            spider, response = self.scheduler.get_task(self)
            try:
                for obj in getattr(response, 'callback')(response):
                    self.scheduler.new_task(spider, obj)
            except Exception as e:
                logger.debug('{} [FAILED]: {}'.format(response.url, str(e)))
                raise