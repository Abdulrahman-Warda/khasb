# -*- coding: utf-8 -*-

from odoo import models, fields

class RepairRequestinherit(models.Model):
    _inherit = 'repair.request'
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id.id,)