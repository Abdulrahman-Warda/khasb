# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DesignRequestinherit(models.Model):
    _inherit = 'design.request'
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id.id,)