# -*- coding: utf-8 -*-
# 导入系统监控视图
from app.views.views_index import IndexHandler
# 导入日志监控视图
from app.views.views_log import LogHandler
# 导入实时监控视图
from app.views.views_real_time import RealTimeHandler

# 配置路由视图映射规则
urls = [
    (r"/", IndexHandler),
    (r"/log/", LogHandler),
    (r"/real/time/", RealTimeHandler),
]
