# coding=utf-8
import logging
from happyspider.utils import walk_modules, iter_spider_classes

logger = logging.getLogger(__name__)


class SpiderLoader(object):
    def __init__(self, project):
        self._project = project
        self._spiders = {}
        self._load_all_spiders()
        logger.debug('加载所有爬虫: ' + str(self.list()))

    def _load_spiders(self, module):
        for spidercls in iter_spider_classes(module):
            self._spiders[spidercls.name] = spidercls

    def _load_all_spiders(self):
        for module in walk_modules(self._project.spiders_module):
            self._load_spiders(module)

    def load(self, spider_name):
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))

    def list(self):
        return list(self._spiders.keys())