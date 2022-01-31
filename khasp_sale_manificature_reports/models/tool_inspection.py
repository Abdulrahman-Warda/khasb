# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ToolInspectionInherit(models.Model):
    _inherit = 'tool.inspection'
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id.id,)