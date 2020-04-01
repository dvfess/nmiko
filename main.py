#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import locale
import logging
import threading
import queue
import worker
import config

start_time = time.time()

# Меняем локаль, что бы разпознавать не локализованную дату из логов
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# Используем  потокобезопасную библиотеку logger для записи результата в файл
fileLogger = logging.getLogger(__name__)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler(config.FILENAME)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logFormatter)
fileLogger.setLevel(logging.INFO)
fileLogger.addHandler(fileHandler)

# Логгер для консоли. Потокобезопасный.
cliLog = logging.getLogger(__name__)
CliHandler = logging.StreamHandler(sys.stdout)
CliHandler.setLevel(logging.INFO)
CliHandler.setFormatter(logFormatter)
cliLog.addHandler(CliHandler)

# Список хостов. Не только ip-адреса
BOXES_IP = [line.strip() for line in open(config.IPFILE, 'r')
            if line.strip() != '']

# Очередь задач. Хостов, в нашем случае.
d = queue.Queue()
for ip in BOXES_IP:
    d.put(ip)


class ThreadWork(threading.Thread):
    '''Класс потока-задачи'''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                host = self.queue.get()
                self.setName(host)
            except Exception:
                break

            try:
                self.result = worker.main(host, config.USER,
                                          config.PASSWORD, cliLog)
                fileLogger.info(self.result)
            except Exception as e:
                fileLogger.critical(e, exc_info=True)
            finally:
                self.queue.task_done()


# <количество потоков> =  минимум из: <количество ip-адресов>, <config.THREADS>
for i in range(min(config.THREADS, d.qsize())):
    thr = ThreadWork(d)
    thr.setDaemon(True)
    thr.start()

d.join()

# Время работы.
print(time.time() - start_time)
