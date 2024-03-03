# import time
import random
import asyncio
# 模拟任务函数，等待10s后，返回0 or 1 但是是随机返回的


async def sleepJob():
    print('sleepJob-开始执行')
    # fuck 这个time 会影响整个事件循环 导致接口也被阻塞了
    # time.sleep(10)
    await asyncio.sleep(2)
    print('sleepJob-执行结束')
    return random.choice([0, 1])
