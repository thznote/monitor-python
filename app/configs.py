# -*- coding: utf-8 -*-
# 操作文件和目录
import os

# 获取当前文件所在的目录
root_path = os.path.dirname(__file__)

# 基本配置
configs = dict(
    debug=False,  # 指定调试，开发者模式：True；生产模式：False
    template_path=os.path.join(root_path, "templates"),  # 指定模板路径
    static_path=os.path.join(root_path, "static")  # 指定静态路径
)

# 数据库配置
mysql_configs = dict(
    db_host="127.0.0.1",  # 主机地址
    db_name="monitor",  # 数据库名称
    db_port=3306,  # 数据库端口
    db_user="root",  # 数据库用户
    db_pwd="root"  # 数据库密码
)
