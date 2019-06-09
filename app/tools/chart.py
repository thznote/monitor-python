# -*- coding: utf-8 -*-
import datetime
from pyecharts import options
from pyecharts.charts import Liquid, Gauge, Pie, Line


# 可视化图表类
class Chart(object):
    # 初始选项
    @property
    def init_opts(self):
        return options.InitOpts(
            width="100%",  # 画布宽度
            height="300px",  # 画布高度
        )

    # 标记线选项
    @property
    def markline_opts(self):
        return options.MarkLineOpts(
            data=[
                options.MarkLineItem(type_="min"),  # 最小值
                options.MarkLineItem(type_="average"),  # 平均值
                options.MarkLineItem(type_="max"),  # 最大值
            ]
        )

    # 标记点选项
    @property
    def markpoint_opts(self):
        return options.MarkPointOpts(
            data=[
                options.MarkPointItem(type_="min"),  # 最小值
                options.MarkPointItem(type_="average"),  # 平均值
                options.MarkPointItem(type_="max"),  # 最大值
            ]
        )

    # 标题选项
    def title_opts(self, title):
        return options.TitleOpts(
            title="{}-{}".format(
                self.dt, title
            ),  # 标题名称
            pos_left="center",  # 标题位置
            title_textstyle_opts=options.TextStyleOpts(
                color="white",  # 标题颜色
                font_size=14,  # 标题大小
            )  # 标题样式
        )

    # 标题选项-无日期
    @staticmethod
    def title_opts_custom(title, pos_left="center", color="black", font_size=14):
        return options.TitleOpts(
            title=title,  # 标题名称
            pos_left=pos_left,  # 标题位置
            title_textstyle_opts=options.TextStyleOpts(
                color=color,  # 标题颜色
                font_size=font_size,  # 标题大小
            )  # 标题样式
        )

    # 水球图
    def liquid_html(self, chart_id, title, val):
        # 实例化
        liquid = Liquid(
            self.init_opts
        )
        # 绑定id
        liquid.chart_id = chart_id
        # 添加参数
        liquid.add("", [round(val / 100, 4)])
        # 全局参数
        liquid.set_global_opts(
            title_opts=self.title_opts(title)
        )
        # 返回图表html代码
        return liquid.render_embed()

    # 仪表图
    def gauge_html(self, chart_id, title, val):
        # 实例化
        gauge = Gauge(
            self.init_opts
        )
        # 绑定id
        gauge.chart_id = chart_id
        # 添加参数
        gauge.add(
            "",
            [("", val)],
            min_=0,
            max_=100
        )
        # 全局参数
        gauge.set_global_opts(
            title_opts=self.title_opts(title),  # 标题选项
            legend_opts=options.LegendOpts(is_show=False),  # 不显示图例组件
        )
        # 返回图表html代码
        return gauge.render_embed()

    # 双饼状图
    def pie_two_html(self, chart_id, title, sub_title1, sub_title2, key1, key2, val1, val2):
        # 实例化饼状图
        pie = Pie(
            self.init_opts
        )
        # 绑定id
        pie.chart_id = chart_id
        # 绑定属性和值
        pie.add(
            sub_title1,
            [list(v) for v in zip(key1, val1)],
            center=["25%", "50%"],
            radius=["30%", "75%"],
            rosetype="area",
            label_opts=options.LabelOpts(is_show=True)
        )
        pie.add(
            sub_title2,
            [list(v) for v in zip(key2, val2)],
            center=["75%", "50%"],
            radius=["30%", "75%"],
            rosetype="area",
            label_opts=options.LabelOpts(is_show=True)
        )
        # 全局参数
        pie.set_global_opts(
            title_opts=self.title_opts(title),  # 标题选项
            legend_opts=options.LegendOpts(is_show=False),  # 不显示图例组件
        )
        # 返回图表html代码
        return pie.render_embed()

    # 折线面积图
    def line_html(self, title, key, val, color=None):
        # 实例化
        line = Line(
            self.init_opts
        )
        # X轴
        line.add_xaxis(key)
        # Y轴
        line.add_yaxis(
            "",
            val,
            markline_opts=self.markline_opts,  # 标记线选项
            markpoint_opts=self.markpoint_opts  # 标记点选项
        )
        # 系列配置
        line.set_series_opts(
            linestyle_opts=options.LineStyleOpts(
                opacity=0.2,  # 透明度
            ),  # 线条样式
            areastyle_opts=options.AreaStyleOpts(
                opacity=0.4,  # 透明度
                color=color  # 颜色
            )  # 面积样式
        )
        # 全局配置
        line.set_global_opts(
            title_opts=self.title_opts_custom(title),  # 标题选项
            datazoom_opts=[options.DataZoomOpts()],  # 缩放选项
            yaxis_opts=options.AxisOpts(
                min_=0,
                max_=100
            ),  # Y轴范围
        )
        # 返回图表html代码
        return line.render_embed()

    # 最小、平均、最大基准折线图
    def line_three_html(self, title, key, val_min, val_max, val_avg):
        # 实例化
        line = Line(
            self.init_opts
        )
        # X轴
        line.add_xaxis(key)
        # Y轴
        line.add_yaxis(
            "最小值",
            val_min,
            is_smooth=True,  # 平滑曲线
            markpoint_opts=self.markpoint_opts  # 标记点选项
        )
        line.add_yaxis(
            "最大值",
            val_max,
            is_smooth=True,  # 平滑曲线
            markpoint_opts=self.markpoint_opts  # 标记点选项
        )
        line.add_yaxis(
            "平均值",
            val_avg,
            is_smooth=True,  # 平滑曲线
            markpoint_opts=self.markpoint_opts  # 标记点选项
        )
        # 全局配置
        line.set_global_opts(
            title_opts=self.title_opts_custom(title, pos_left="left"),  # 标题选项
            datazoom_opts=[options.DataZoomOpts()],  # 缩放选项
            yaxis_opts=options.AxisOpts(
                min_=0,
                max_=100
            ),  # Y轴范围
        )
        # 返回图表html代码
        return line.render_embed()

    # 日期时间方法
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
