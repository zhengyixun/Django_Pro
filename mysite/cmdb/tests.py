# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# 子进程
import multiprocessing
import time

if __name__ == '__main__':
    p = multiprocessing.Process()
    p.start()
    p.deamon = True
    num = 0
    while num < 10:
        num = num + 1
        print '这是主进程,第',num
        time.sleep(1)
    else:
        # 停止子进程
        p.terminate()
