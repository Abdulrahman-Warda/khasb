# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseInherit(models.Model):
    _inherit = 'product.template'
    design = fields.Boolean(string='Design',default=False)
    prod_number = fields.Char(string="Product Number")