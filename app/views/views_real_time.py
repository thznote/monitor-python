# -*- coding: utf-8 -*-
import json
import tornado.websocket
from app.tools.monitor import Monitor


# 实时监控类
class RealTimeHandler(tornado.websocket.WebSocketHandler):
    # 定义连接池
    waiters = set()

    def get_compression_options(self):
        return {}

    # 1.建立连接
    def open(self):
        RealTimeHandler.waiters.add(self)

    # 2.关闭连接
    def on_close(self):
        RealTimeHandler.waiters.remove(self)

    # 发送修改
    @classmethod
    def send_updates(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except Exception as e:
                print(e)

    # 3.发送消息
    def on_message(self, message):
        try:
            m = Monitor()
            data = dict()
            if message == "system":
                data = dict(
                    mem=m.mem(),
                    swap=m.swap(),
                    cpu=m.cpu(),
                    disk=m.disk(),
                    net=m.net(),
                    dt=m.dt()
                )
            RealTimeHandler.send_updates(json.dumps(data))
        except Exception as e:
            print(e)
