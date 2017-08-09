# coding=utf-8


class DefaultSettings(dict):
    def __init__(self, **kwargs):
        self['SPIDERS_MODULE'] = 'spiders'  # 爬虫类所在模块
        self['SETTINGS_MODULE'] = 'settings'  # settings模块
        self['SCHEDULER_WAIT_SECS'] = 0.5  # 调度器等待循环检测退出条件间隔秒数
        self['SCHEDULER_WAIT_TIMES'] = 10  # 调度器等待循环检测退出条件最大次数
        self['CRAWLER_NUM'] = 8  # Crawler组件线程数
        self['PARSER_NUM'] = 8  # Parser组件线程数
        self['TRANSPORTER_NUM'] = 8  # Transporter组件线程数
        self['TRANSPORTER_DRIVERS'] = ['happyspider.transporter.ConsoleDriver']  # Transporter组件处理器,为空则调用ConsoleDriver做标准输出
        self['PHANTOMJS_PROC'] = 4  # Phantomjs进程数
        self['PHANTOMJS_SETTING'] = {}  # Phantomjs执行环境配置
        super(DefaultSettings, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value