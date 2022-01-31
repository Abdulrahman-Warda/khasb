# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_company_modification(models.Model):
    _inherit = 'res.company'

    company_arabic_name = fields.Char(string="Arabic Name", required=False, )
    # com_type = fields.Selection(string="Type", selection=[('sahood', 'SAHOOD'), ('khasp', 'Khasp'), ] )
    # state = fields.Selection(string="Type", selection=[('sahood', 'SAHOOD'), ('khasp', 'Khasp') ], required=False, )