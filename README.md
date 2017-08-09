# happyspider
A simple spider framework for Python
# Install
`cd happyspider`

`pip install -r requirements.txt`

`bash setup.sh`
# Project
```
project
└───spiders
│   │   __init__.py
│   │   demo.py
|___setting.py
|___transporter.py (optional)
```
# demo.py
```py
# coding=utf-8
from happyspider import Spider, Request, Item
from lxml import etree

class Demo(Spider):
    name = 'demo'
    start_urls = [
        'https://github.com/jellycoming',
    ]

    def parse(self, response):
        s = etree.HTML(response.html)
        title = s.xpath('//title/text()')
        yield Item(title=title[0])
        yield Request(url=response.url, callback=self.parse_more)

    def parse_more(self, response):
        s = etree.HTML(response.html)
        title = s.xpath('//title/text()')
        yield Item(title=title[0], name=self.name)
```
# settings.py
```py
# coding=utf-8

# 爬虫类所在模块
SPIDERS_MODULE = 'spiders'
# Crawler组件线程数
CRAWLER_NUM = 8
# Parser组件线程数
PARSER_NUM = 8
# Transporter组件线程数
TRANSPORTER_NUM = 8
# Transporter组件处理器,为空则调用ConsoleDriver做标准输出
TRANSPORTER_DRIVERS = [
    'MyDriver',
    'happyspider.transporter.ConsoleDriver',
]
# Phantomjs执行环境配置
PHANTOMJS_SETTING = dict(
    executable_path='/usr/local/bin/phantomjs',
    service_args=["--webdriver-loglevel=ERROR"],
    service_log_path='/tmp/ghostdriver.log'
)
# Phantomjs进程数
PHANTOMJS_PROC = 4
```
# transporter.py
```py
# coding=utf-8
import json
from happyspider.transporter import Driver

class MyDriver(Driver):
    def __init__(self):
        super(MyDriver, self).__init__(thread_safety=True)

    def transport(self, spider, item):
        item.spider = spider.name
        with open('/tmp/happyspider.txt', 'a') as f:
            json.dump(item, f)
```
# Run
`cd /path/to && happyspider run --debug`

