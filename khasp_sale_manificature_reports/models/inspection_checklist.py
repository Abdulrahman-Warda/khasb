# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RepairRequest(models.Model):
    _inherit = 'inspection.checklist'
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id.id,)