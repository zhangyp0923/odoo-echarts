# -*- coding: utf-8 -*-
'''
Created on 2017年5月18日
@author: allen
pyecharts version:0.5.8
'''
from odoo import api, fields, models, tools, _
import time
from pyecharts import Bar
from pyecharts import Pie
import os
import logging

_logger = logging.getLogger(__name__)


class DataTemplate(models.Model):
    _name = 'data.template'
    _description = u'数据模板'

    name = fields.Char('名称')
    line_ids = fields.One2many('data.template.line', 'temp_id', string='明细行')

    pie_charts = fields.Text('饼状图')
    bar_charts = fields.Text('柱状图')

    @api.multi
    def action_generate_charts(self):
        attr = []
        v1 = []
        for obj in self.line_ids:
            attr.append(obj.key)
            v1.append(obj.value)
        pie = Pie(self.name)
        pie.add("", attr, v1, radius=[30, 75], label_text_color=None, is_label_show=True, legend_orient='vertical',
                legend_pos='right')
        pie_charts_name = 'pie_charts' + str(time.time()) + '.html'
        pie.render(pie_charts_name)
        self.pie_charts = open(pie_charts_name, 'rb').read()
        os.remove(pie_charts_name)
        bar = Bar(self.name)
        bar.add('', attr, v1, xaxis_interval=0)
        bar_charts_name = 'bar_charts' + str(time.time()) + '.html'
        bar.render(bar_charts_name)
        self.bar_charts = open(bar_charts_name, 'rb').read()
        os.remove(bar_charts_name)


class DataTemplateLine(models.Model):
    _name = 'data.template.line'
    _description = u'数据模板'

    temp_id = fields.Many2one('data.template', '模板')
    key = fields.Char('键')
    value = fields.Float('值')


