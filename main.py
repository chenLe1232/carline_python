from typing import Union
import asyncio

from fastapi import FastAPI
from jobs.sleep import sleepJob
from models import User


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = User.get_or_none(User.id == user_id)
    if user:
        return {
            "username": user.username,
            "password": user.password,
            "id": user.id,
            "email": user.email,
        }
    else:
        user = User.create(username='lechen', password='test', email='aaa')
        return {
            "username": user.username,
            "password": user.password,
            "id": user.id,
            "email": user.email,
        }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# job执行函数 用于测试 请求方法为get 调用sleep函数 等待10s后返回0 or 1 返回 1则表示成功 返回0则表示失败
# 但是这个函数是同步的 所以先接收所有请求
# 如果查表存在status为running的数据 则不做任何操作
# 如果不存在 status为running的数据 则查找status为wait 最小id的数据 修改status为running，执行sleep函数 然后修改status为success或者failed
# 执行完成后 递归调用自己 直到没有status为wait的数据


async def run_job():
    print('run_job-开始执行')
    # 先判断是否有status为running的数据
    user = User.get_or_none(User.status == 'running')
    # 如果有 则不做任何操作
    if user:
        return
    # 如果没有 则查找status为wait 最小id的数据 修改status为running
    user = User.get_or_none(User.status == 'wait')
    if user:
        user.status = 'running'
        user.save()
        # 执行sleep函数
        result = await sleepJob()
        print('result-执行情况', result)
        # 修改status为success或者failed
        user.status = 'success' if result else 'failed'
        user.save()
        # 递归调用自己 直到没有status为wait的数据
        await run_job()
    else:
        # 输出彩色的日志
        print('\033[1;31;40m run_job-没有status为wait的数据了 \033[0m')
        return

# 定义一个检查是否存在status为running or wait的数据的函数 计算所有的数量 如果没有则返回0 如果有则返回所有的数量


def check_job():
    # 计算所有的数量
    count = User.select().where(
        User.status.in_(['running', 'wait'])).count()
    print('check_job-执行情况', count)
    return count

# 插入一条数据 模拟任务参数


def insert_job():
    print('insert_job-开始执行 插入数据')
    user = User.create(username='lechen', password='test',
                       email='aaa', status='wait')
    return user.id

# 定义一个调试方法， 将所有的数据的status修改为failed


@app.get("/debug")
def debug():
   # 查询所有不是failed or success的数据 修改为failed
    users = User.select().where(
        User.status.not_in(['failed', 'success']))
    for user in users:
        user.status = 'failed'
        user.save()
    return {"msg": "ok"}

# 获取所有的数据 返回一个列表


@app.get("/infos")
def infos():

    users = User.select().where(
        User.status.not_in(['failed', 'success']))
    result = []
    for user in users:
        result.append({
            "username": user.username,
            "password": user.password,
            "id": user.id,
            "email": user.email,
            "status": user.status,
        })
    return result


async def fuck_job():
    count = check_job()
    insert_job()
    if not count:
        print('当前count为0 开始执行run_job', count)
        await run_job()  # 创建一个新的任务来执行 run_job 函数
    # 彩色输出 已有执行中or 等待中的人物
    print(" 已有执行中or 等待中的人物")


@app.get("/job")
async def main_job():
    asyncio.create_task(fuck_job())
    count = check_job()
    return {"msg": "ok:" + "预期排队:"+str(count)}
