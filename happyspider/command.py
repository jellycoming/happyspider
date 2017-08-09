# coding=utf-8


class Commands(object):
    def __init__(self, sched):
        self._sched = sched
        super(Commands, self).__init__()

    def run(self):
        return self._sched.run()

    def list(self):
        return self._sched.list()