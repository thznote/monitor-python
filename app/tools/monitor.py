# -*- coding: utf-8 -*-
# 导入日期时间库
import datetime
# 导入系统信息库
import psutil


# 定义一个专门用于获取系统信息的类
class Monitor(object):
    # 专门用于单位转化的方法
    @staticmethod
    def bytes_to_gb(data, key=""):
        if key == "percent":
            # 百分比直接返回
            return data
        else:
            # 字节转化为GB，保留两位小数
            return round(data / (1024 ** 3), 2)

    # 专门获取CPU信息
    @staticmethod
    def cpu():
        # percpu：True获取每个CPU的使用率，False获取平均使用率
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),  # 平均使用率
            percent_per=psutil.cpu_percent(interval=0, percpu=True),  # 单独使用率
            num_p=psutil.cpu_count(logical=False),  # 物理CPU核心数
            num_l=psutil.cpu_count(logical=True)  # 逻辑CPU核心数
        )
        return data

    # 专门获取内存信息
    def mem(self):
        # 内存信息
        info = psutil.virtual_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),  # 内存总量
            used=self.bytes_to_gb(info.used),  # 内存使用量
            free=self.bytes_to_gb(info.free),  # 内存剩余量
            percent=info.percent  # 内存使用率
        )
        return data

    # 专门获取交换分区/文件信息
    def swap(self):
        # 交换文件/分区信息
        info = psutil.swap_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),  # 交换分区总量
            free=self.bytes_to_gb(info.free),  # 交换分区剩余量
            used=self.bytes_to_gb(info.used),  # 交换分区使用量
            percent=info.percent  # 交换分区使用率
        )
        return data

    # 专门获取磁盘信息
    def disk(self):
        # 专门获取磁盘分区信息
        info = psutil.disk_partitions()
        # 列表推导式
        data = [
            dict(
                device=v.device,  # 设备名称
                mountpoint=v.mountpoint,  # 挂载点
                fstype=v.fstype,  # 文件系统类型
                opts=v.opts,  # 操作选项
                used={
                    key: self.bytes_to_gb(val, key)
                    for key, val in psutil.disk_usage(v.mountpoint)._asdict().items()
                }  # 使用情况
            )
            for v in info if 'rw' in v.opts
        ]
        # if v.opts == 'rw,fixed'  # 获取可读可写的固定磁盘
        return data

    # 专门获取网络信息
    @staticmethod
    def net():
        # 获取地址信息
        address = psutil.net_if_addrs()
        # 处理地址信息
        address_info = {
            k: [
                dict(
                    family=val.family.name,  # 协议地址族名称
                    address=val.address,  # IP地址
                    netmask=val.netmask,  # 子网掩码
                    broadcast=val.broadcast  # 广播地址
                )
                for val in v if val.family.name == "AF_INET"  # 过滤IPV4协议
            ]
            for k, v in address.items()
        }
        # 获取网络信息
        io = psutil.net_io_counters(pernic=True)
        # 处理网络信息
        data = [
            dict(
                name=k,  # 网卡名称
                bytes_sent=v.bytes_sent,  # 发送字节数
                bytes_recv=v.bytes_recv,  # 接收字节数
                packets_sent=v.packets_sent,  # 发送包数
                packets_recv=v.packets_recv,  # 接收包数
                **address_info[k][0]
            )
            for k, v in io.items() if len(address_info[k]) > 0
        ]
        return data

    # 时间戳转化为时间字符方法
    @staticmethod
    def td(tm):
        dt = datetime.datetime.fromtimestamp(tm)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 获取日期时间
    @staticmethod
    def dt():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 专门获取最近开机时间
    def lasted_start_time(self):
        # 时间戳
        return self.td(psutil.boot_time())

    # 专门获取系统登录用户
    def login_users(self):
        # 获取系统登录用户
        users = psutil.users()
        # 处理系统登录用户
        data = [
            dict(
                name=v.name,  # 登录用户
                terminal=v.terminal,  # 登录终端
                host=v.host,  # 登录主机
                started=self.td(v.started),  # 登录时间
                pid=v.pid  # 进程ID
            )
            for v in users
        ]
        return data
