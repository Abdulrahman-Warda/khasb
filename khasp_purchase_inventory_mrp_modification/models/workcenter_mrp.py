# -*- coding: utf-8 -*-
from odoo import models, fields, api
class khasp_work_center_modification(models.Model):
    _inherit = 'mrp.workcenter'

    worker_ids = fields.Many2many(comodel_name="res.users", string="Workers", )
