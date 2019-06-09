# -*- coding: utf-8 -*-
import mysql.connector  # 数据库连接驱动
from sqlalchemy import create_engine  # 创建引擎
from sqlalchemy.orm import sessionmaker  # 创建会话
from app.configs import mysql_configs  # 数据库配置


class ORM:
    # 会话方法
    @classmethod
    def db(cls):
        link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8".format(
            **mysql_configs
        )
        # 创建引擎
        engine = create_engine(
            link,
            encoding="utf-8",
            echo=False,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': 'utf8'}
        )
        # 创建会话
        session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )
        return session()
