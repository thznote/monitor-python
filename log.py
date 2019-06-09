# -*- coding: utf-8 -*-
import time
import datetime
from app.models.models import Cpu, Mem, Swap
from app.tools.monitor import Monitor
from app.tools.sync_orm import ORM


# 日期时间函数
def dt():
    now_date_time = datetime.datetime.now()  # 日期时间
    now_date = now_date_time.date()  # 日期
    now_time = now_date_time.time()  # 时间
    return now_date, now_time, now_date_time


# 定义保存日志的函数
def save_log():
    m = Monitor()
    cpu_info, mem_info, swap_info = m.cpu(), m.mem(), m.swap()
    now_date, now_time, now_date_time = dt()
    # 1.创建会话
    session = ORM.db()
    try:
        # CPU
        cpu = Cpu(
            percent=cpu_info["percent_avg"],
            create_date=now_date,
            create_time=now_time,
            create_dt=now_date_time
        )
        # 内存
        mem = Mem(
            percent=mem_info['percent'],
            total=mem_info['total'],
            used=mem_info['used'],
            free=mem_info['free'],
            create_date=now_date,
            create_time=now_time,
            create_dt=now_date_time
        )
        # 交换分区
        swap = Swap(
            percent=swap_info['percent'],
            total=swap_info['total'],
            used=swap_info['used'],
            free=swap_info['free'],
            create_date=now_date,
            create_time=now_time,
            create_dt=now_date_time
        )
        # 提交数据
        session.add(cpu)
        session.add(mem)
        session.add(swap)
    except Exception as e:
        print(e)
        # 异常回滚
        session.rollback()
    else:
        # 正常提交
        session.commit()
    finally:
        # 关闭会话
        session.close()


if __name__ == "__main__":
    while True:
        # now_date, now_time, now_date_time = dt()
        # print("开始时间：{}".format(now_date_time))
        save_log()
        # print("结束时间：{}".format(now_date_time))
        time.sleep(5)  # 每隔5秒采集一次
