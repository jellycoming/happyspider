# coding=utf-8


class Request(object):
    def __init__(self, url, callback, method='GET', params=None, data=None,
                 headers=None, cookies=None, driver=None):
        self.url = url
        assert callable(callback), 'Callback must be callable.'
        self.callback = callback
        self.method = str(method).upper()
        self.params = params or {}
        self.data = data or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.driver = driver
        super(Request, self).__init__()


class Response(object):
    def __init__(self, url, html, callback, status_code=None):
        self.url = url
        self.html = html
        self.callback = callback
        self.status_code = status_code or 200
        super(Response, self).__init__()


class Item(dict):
    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value