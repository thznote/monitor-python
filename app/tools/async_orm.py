# -*- coding: utf-8 -*-
# 进程、线程、上下文
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

# orm相关
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base as sa_declarative_base
from sqlalchemy.orm import sessionmaker

# tornado相关
from tornado.concurrent import Future, chain_future
from tornado.ioloop import IOLoop

__all__ = ['SessionMixin', 'set_max_workers', 'as_future',
           'make_session_factory', 'declarative_base']


class MissingFactoryError(Exception):
    pass


# 异步执行
class _AsyncExecution:
    """
    围绕线程池执行器的封装。该类不在外部实例化，但在内部我们只是将其用作包装线程池执行器，以便控制池大小并使用'as_future'作为公共方法。
    参数
    ----------
    max_workers: int
        线程池工作数量
    """

    def __init__(self, max_workers=None):
        self._max_workers = max_workers or multiprocessing.cpu_count()
        self._pool = None

    def set_max_workers(self, count):
        if self._pool:
            self._pool.shutdown(wait=True)

        self._max_workers = count
        self._pool = ThreadPoolExecutor(max_workers=self._max_workers)

    def as_future(self, query):
        """
        使SQLAlchemy查询对象异步化

        参数
        ----------
            query: sqlalchemy.orm.query.Query
                要执行的sqlalchemy查询对象
        返回
        -------
            tornado.concurrent.Future
            一个获取查询记录的'Future'对象，tornado可以用await/yield调用
        """
        if not self._pool:
            self._pool = ThreadPoolExecutor(max_workers=self._max_workers)

        old_future = self._pool.submit(query)
        new_future = Future()

        IOLoop.current().add_future(old_future,
                                    lambda f: chain_future(f, new_future))

        return new_future


# 会话工厂
class SessionFactory:
    """
    SessionFactory是围绕sqlAlchemy提供的扩展类。这里的目的是让用户在会话级别工作而不是引擎和连接。
    参数
    ----------
        database_url: str
            数据库连接
        pool_size: int
            连接池大小
        use_native_unicode: bool
            启用/禁用本机Unicode编码；仅在以下情况下使用的驱动是psycopg2
        engine_events: List[Tuple[str, Callable]]
            订阅引擎事件的元组(name, listener_function)列表
        session_events: List[Tuple[str, Callable]]
            订阅会话事件的元组(name, listener_function)列表
    """

    def __init__(self, database_url, pool_size=None, use_native_unicode=True,
                 engine_events=None, session_events=None):
        self._database_url = make_url(database_url)
        self._pool_size = pool_size
        self._engine_events = engine_events
        self._session_events = session_events
        self._use_native_unicode = use_native_unicode

        self._engine = None
        self._factory = None

        self._setup()

    def _setup(self):
        kwargs = {}

        if self._database_url.get_driver_name() == 'postgresql':
            kwargs['use_native_unicode'] = self._use_native_unicode

        if self._pool_size is not None:
            kwargs['pool_size'] = self._pool_size

        self._engine = create_engine(self._database_url, **kwargs)

        if self._engine_events:
            for (name, listener) in self._engine_events:
                event.listen(self._engine, name, listener)

        self._factory = sessionmaker()
        self._factory.configure(bind=self._engine)

    def make_session(self):
        session = self._factory()

        if self._session_events:
            for (name, listener) in self._session_events:
                event.listen(session, name, listener)

        return session

    @property
    def engine(self):
        return self._engine


# 会话中间件
class SessionMixin:
    _session = None

    # 使用上下文会话
    @contextmanager
    def make_session(self, session_factory):
        session = None

        try:
            session = self._make_session(session_factory)

            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        else:
            session.commit()
        finally:
            if session:
                session.close()

    # 关闭连接
    def on_finish(self):
        next_on_finish = None

        try:
            next_on_finish = super(SessionMixin, self).on_finish
        except AttributeError:
            pass

        if self._session:
            self._session.commit()
            self._session.close()

        if next_on_finish:
            next_on_finish()

    # 使用会话
    @property
    def session(self, session_factory):
        if not self._session:
            self._session = self._make_session(session_factory)
        return self._session

    # 创建会话
    def _make_session(self, session_factory):
        factory = self.application.settings.get(session_factory)
        if not factory:
            raise MissingFactoryError()

        return factory.make_session()


_async_exec = _AsyncExecution()

as_future = _async_exec.as_future

set_max_workers = _async_exec.set_max_workers


# 创建会话工厂
def make_session_factory(database_url,
                         pool_size=None,
                         use_native_unicode=True,
                         engine_events=None,
                         session_events=None):
    return SessionFactory(database_url, pool_size, use_native_unicode,
                          engine_events, session_events)


# 创建基类
class _declarative_base:
    def __init__(self):
        self._instance = None

    def __call__(self):
        if not self._instance:
            self._instance = sa_declarative_base()
        return self._instance


declarative_base = _declarative_base()
