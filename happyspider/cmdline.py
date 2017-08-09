# coding=utf-8
#
# 初始化项目的时候会检测当前目录下是否有可导入的spiders模块及settings模块;
# 将遍历spiders模块及其子模块下的所有happyspider.spider.Spider类并加载;
# 如果未检测到settings模块, 项目将使用happyspider.settings.Settings作为默认配置;

import click
import os
import sys
from Queue import Queue
from happyspider import log
from happyspider.project import Project
from happyspider.scheduler import Scheduler
from happyspider.command import Commands
from happyspider.utils import check_module


@click.command()
@click.argument('cmd')
@click.argument('spiders', type=str, nargs=-1)
@click.option('--path', help='Specify project root path')
@click.option('--debug', is_flag=True, show_default=True, help='Debug mode')
def execute(cmd, **kwargs):
    _setup_logger(debug=kwargs.get('debug'))
    sched = Scheduler(project=Project(**kwargs), request_queue=Queue(), response_queue=Queue(), item_queue=Queue())
    commands = Commands(sched)
    try:
        rv = getattr(commands, cmd)()
        if type(rv) == str:
            click.echo(rv)
        else:
            try:
                for r in rv:
                    click.echo(r)
            except TypeError:
                pass
    except AttributeError:
        click.echo('Unsupported cmd [{}]. Only {} accepted'.format(cmd, _supported_commands()))


def _setup_logger(debug=False):
    level = log.DEBUG if debug else log.ERROR
    log.set_stream_handler(level=level)
    log.disable_logger('requests')
    log.disable_logger('selenium')


def _supported_commands():
    return [method for method in dir(Commands) if callable(getattr(Commands, method)) and not method.startswith('_')]