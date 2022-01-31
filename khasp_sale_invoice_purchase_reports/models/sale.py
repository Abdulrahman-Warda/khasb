# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_sale_modification(models.Model):
    _inherit = 'sale.order'
    signature = fields.Many2one(comodel_name="hr.employee", string="signature", required=False, )
    offer_period = fields.Integer(string="Offer period", required=False, )
    general_conditions = fields.Text(string="General Conditions", required=False, )
    total_unit_price_tax = fields.Float(string="",  compute='get_total_unit_price' )


    @api.depends('order_line')
    def get_total_unit_price(self):
        total = 0
        for rec in self:
            for line in rec.order_line:
                total += line.unit_price_tax
            rec.total_unit_price_tax = total

class khasp_sale_line_modification(models.Model):
    _inherit = 'sale.order.line'
    total_without_tax = fields.Float(string="",  compute='get_residual_fields', )
    unit_price_tax = fields.Float(string="",  compute='get_residual_fields' )
    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def get_residual_fields(self):
        for rec in self:
            total_tax = 0
            for tax in rec.tax_id:
                total_tax += tax.amount
            rec.total_without_tax = rec.product_uom_qty * rec.price_unit
            rec.unit_price_tax = (rec.price_unit * (total_tax/100))