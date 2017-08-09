# coding=utf-8
import sys
import inspect
from threading import Thread
from importlib import import_module
from pkgutil import iter_modules, find_loader


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


def run_in_thread(func, *args, **kwargs):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()
    return thread


def check_module(module):
    return True if find_loader(module) else False


def walk_modules(path):
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def find_class(path):
    """
    找到path路径中指定的类, 如happyspider.transporter.ConsoleDriver, 从happyspider.transporter模块中找到ConsoleDriver并返回
    :param path:
    :return: classobj
    """
    if '.' not in path:
        raise TypeError('Invalid relative module path: ' + path)
    package, cls = path.rsplit('.', 1)
    try:
        module = sys.modules[package] if package in sys.modules else import_module(package)
        return getattr(module, cls)
    except AttributeError:  # module has no attribute `cls`
        raise


def iter_spider_classes(module):
    from happyspider.spider import Spider

    for obj in vars(module).values():
        if inspect.isclass(obj) and \
           issubclass(obj, Spider) and \
           obj.__module__ == module.__name__ and \
           getattr(obj, 'name', None):
            yield obj


def call_func(obj, func, *args, **kwargs):
    getattr(obj, func)(*args, **kwargs)