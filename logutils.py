#!/usr/bin/env python
#-*- coding:utf-8 -*-
import logging
from logging import Logger, _srcfile
from logging.handlers import TimedRotatingFileHandler
import multiprocessing
import time
from multiprocessing import queues, Pool
import os
import sys
import signal

def LogHandle(sig, frame):
    logger.info("Logger 结束")


class MoLogging(Logger):

    def __init__(self, name, level=logging.NOTSET):
        super(MoLogging, self).__init__(name, level)
        self.queue = queues.Queue()
        self.process = multiprocessing.Process(target=MoLogging.consume_handle, args=(self,))

    def _log(self, level, msg, args, exc_info=None, extra=None):
        if _srcfile:
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.queue.put(record)

    @staticmethod
    def consume_handle(self):
        signal.signal(signal.SIGINT, LogHandle) # 子进程忽视一下中断信号
        signal.signal(signal.SIGQUIT, LogHandle)
        while True:
            print os.getpid()
            try:
                record = self.queue.get(timeout=3)
                Logger.handle(self, record)
            except queues.Empty:
                pass
            except Exception as e:
                print "game over hahaha"
                break

    def inithandle(self):
        self.process.start()

    def is_closed(self):
        return self.is_close

    def close(self):
        self.queue.put('end')


if __name__ == "__main__":
    def task(i):
        for j in range(10000):
            logger.info('%d' % j)
    logger = MoLogging('hahaha')
    handle1 = TimedRotatingFileHandler('a.log')
    handle2 = TimedRotatingFileHandler('b.log')
    logger.addHandler(handle1)
    logger.addHandler(handle2)
    logger.inithandle()
    pool = Pool(20)
    for i in range(20):
        pool.apply(task, (i,))
    time.sleep(10)
    logger.close()