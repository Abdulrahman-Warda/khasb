# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_partner_modification(models.Model):
    _inherit = 'res.partner'
    customer_type = fields.Selection(string="Customer Type", selection=[('governmental', 'Governmental'), ('private', 'Private'), ], required=False, )
    # supplier_code = fields.Char(string="Code", required=False, )