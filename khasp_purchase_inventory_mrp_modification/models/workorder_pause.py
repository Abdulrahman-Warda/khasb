# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
class khasp_workorder_pause_modification(models.Model):
    _name = 'workorder.pause'

    workorder_ref = fields.Many2one(comodel_name="mrp.workorder", string="Work Order ID")
    pause_time = fields.Datetime(string="Pause Time", default=datetime.now(), )
    products_no = fields.Integer(string="Number of finished Products", required=False, )
    reason = fields.Text(string="Reason", required=False, )
