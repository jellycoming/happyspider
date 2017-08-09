# coding=utf-8
import os
import sys
import logging
from happyspider.utils import check_module, import_module
from happyspider.settings import DefaultSettings

logger = logging.getLogger(__name__)


class Project(object):
    """
    用于封装用户爬虫项目的相关信息
    :param path: 项目路径, 会被添加到sys.path, 并在该路径下搜索spiders及settings模块
    :param spiders: 等待被执行的爬虫列表, 默认为空, 表示执行所有爬虫
    :param debug: 测试模式
    """
    def __init__(self, **kwargs):
        logger.debug('初始化项目信息...')
        self._settings = DefaultSettings()
        self._root_path = kwargs.get('path') or os.getcwd()
        self._waiting = kwargs.get('spiders')
        self._debug = kwargs.get('debug')

        if self._root_path not in sys.path:
            sys.path.append(self._root_path)

        try:
            module = import_module(self._settings.SETTINGS_MODULE)
            logger.debug('加载自定义配置')
            for key in dir(module):
                if key.isupper():
                    self._settings[key] = getattr(module, key)
        except ImportError:
            pass

        if not check_module(self._settings.SPIDERS_MODULE):
            raise ImportError('Spiders module `{}` not found in path: {}'.format(self._settings.SPIDERS_MODULE, self._root_path))

        logger.debug('初始化项目信息完成: ' + str(self))

    @property
    def root_path(self):
        return self._root_path

    @property
    def debug(self):
        return self._debug

    @property
    def spiders_module(self):
        return self._settings.SPIDERS_MODULE

    @property
    def waiting(self):
        return self._waiting

    @property
    def settings(self):
        return self._settings

    def __str__(self):
        return 'root_path: {}, spiders_module: {}, waiting: {}, debug: {}'\
            .format(self.root_path, self.spiders_module, self.waiting, self.debug)