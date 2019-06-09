# -*- coding: utf-8 -*-
import tornado.web
from app.tools.monitor import Monitor
from app.tools.async_orm import SessionMixin


# 公共视图
class CommonHandler(tornado.web.RequestHandler, SessionMixin):
    @staticmethod
    def progress_status(val):
        data = ""
        if 0 <= val < 25:
            data = " bg-success"  # 绿色
        if 25 <= val < 50:
            data = ""
        if 50 <= val < 75:
            data = " bg-warning"  # 橙色
        if 75 <= val <= 100:
            data = " bg-danger"  # 红色
        return data

    # 最近开始时间
    @property
    def started(self):
        m = Monitor()
        return m.lasted_start_time()

    # 最近登录用户
    @property
    def users(self):
        m = Monitor()
        return m.login_users()
