# -*- coding: utf-8 -*-
# 导入工厂函数
from sqlalchemy.ext.declarative import declarative_base
# 导入字段类型
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, DATE, TIME, DATETIME
# 导入创建字段的类
from sqlalchemy import Column

# 导入数据库配置
# from app.configs import mysql_configs

# 创建基类
Base = declarative_base()
# 创建元类
metadata = Base.metadata


# 内存统计模型
class Mem(Base):
    __tablename__ = "mem"  # 表名称
    id = Column(BIGINT, primary_key=True)  # 主键编号
    percent = Column(DECIMAL(6, 2))  # 内存使用率
    total = Column(DECIMAL(8, 2))  # 内存总量
    used = Column(DECIMAL(8, 2))  # 内存使用量
    free = Column(DECIMAL(8, 2))  # 内存剩余量
    create_date = Column(DATE)  # 创建日期
    create_time = Column(TIME)  # 创建时间
    create_dt = Column(DATETIME)  # 创建日期时间


# 交换分区统计
class Swap(Base):
    __tablename__ = "swap"  # 表名称
    id = Column(BIGINT, primary_key=True)  # 主键编号
    percent = Column(DECIMAL(6, 2))  # 交换分区使用率
    total = Column(DECIMAL(8, 2))  # 交换分区总量
    used = Column(DECIMAL(8, 2))  # 交换分区使用量
    free = Column(DECIMAL(8, 2))  # 交换分区剩余量
    create_date = Column(DATE)  # 创建日期
    create_time = Column(TIME)  # 创建时间
    create_dt = Column(DATETIME)  # 创建日期时间


# CPU统计
class Cpu(Base):
    __tablename__ = "cpu"  # 表名称
    id = Column(BIGINT, primary_key=True)  # 主键编号
    percent = Column(DECIMAL(6, 2))  # CPU使用率
    create_date = Column(DATE)  # 创建日期
    create_time = Column(TIME)  # 创建时间
    create_dt = Column(DATETIME)  # 创建日期时间


def create_table():
    mysql_configs = dict(
        db_host="127.0.0.1",  # 主机地址
        db_name="monitor",  # 数据库名称
        db_port=3306,  # 数据库端口
        db_user="root",  # 数据库用户
        db_pwd="root"  # 数据库密码
    )
    # 1.导入数据库连接驱动
    import mysql.connector
    # 2.导入创建引擎的函数
    from sqlalchemy import create_engine
    # 3.连接格式：mysql+驱动名称://用户:密码@主机:端口/数据库名称
    link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
        **mysql_configs
    )
    # 4.创建连接引擎，encoding定义编码，echo是(True)否(False)输出日志
    engine = create_engine(link, encoding="utf-8", echo=True)
    # 5.将模型映射为数据表
    metadata.create_all(engine)


if __name__ == "__main__":
    # 创建数据表
    create_table()
