# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_company_type_modification(models.Model):
    _inherit = 'res.company'
    state = fields.Selection(string="Type", selection=[('sahood', 'SAHOOD'), ('khasp', 'Khasp')], required=False, )