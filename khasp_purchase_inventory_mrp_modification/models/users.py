# -*- coding: utf-8 -*-

from odoo import models, fields, api


class khasp_users_modification(models.Model):
    _inherit = 'res.users'
    # is_factory_manger = fields.Boolean(
    #     default=lambda self: self.env.user.has_group(
    #         'mrp.group_mrp_manager'
    #     ))

    work_center_ids = fields.Many2many(comodel_name="mrp.workcenter", relation="mrp_workcenter_users",string="work center")
