# coding=utf-8
import redis


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name='main', namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item, key=None):
        """Put item into the queue."""
        k = key or self.key
        self.__db.rpush(k, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def delete(self, key):
        """delete key"""
        return self.__db.delete(key)

    def ltrim(self, key, start, end):
        return self.__db.ltrim(key, start, end)
