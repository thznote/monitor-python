# -*- coding: utf-8 -*-
from app.views.views_common import CommonHandler
from app.tools.monitor import Monitor
from app.tools.chart import Chart


# 定义一个首页视图
class IndexHandler(CommonHandler):
    async def get(self):
        # 实例化系统信息类
        monitor = Monitor()
        # 实例化可视化图表类
        chart = Chart()
        # CPU信息
        cpu_info = monitor.cpu()
        # 内存信息
        mem_info = monitor.mem()
        # 交换分区
        swap_info = monitor.swap()
        # 网络信息
        net_info = monitor.net()
        # 磁盘信息
        disk_info = monitor.disk()
        # 网络信息
        net_pie = [
            chart.pie_two_html(
                "net{}".format(k + 1),
                "{}网卡信息".format(v["name"]),
                "收发包数统计",
                "收发字节统计",
                ["收包数", "发包数"],
                ["收字节", "发字节"],
                [v["packets_recv"], v["packets_sent"]],
                [v["bytes_recv"], v["bytes_sent"]],
            )
            for k, v in enumerate(net_info) if v["packets_recv"] and v['packets_sent']
        ]
        # 渲染视图
        self.render(
            "index.html",
            data=dict(
                title="系统监控",
                cpu_info=cpu_info,
                mem_info=mem_info,
                swap_info=swap_info,
                net_info=net_info,
                disk_info=disk_info,
                cpu_liquid=chart.liquid_html("cpu_avg", "CPU平均使用率", cpu_info['percent_avg']),
                mem_gauge=chart.gauge_html("mem", "内存使用率", mem_info['percent']),
                swap_gauge=chart.gauge_html("swap", "交换分区使用率", mem_info['percent']),
                net_pie=net_pie,
            )
        )
