# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_invoice_modification(models.Model):
    _inherit = 'account.invoice'
    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale ID", compute='get_sale_id' )
    letter_number = fields.Integer(string="Letter Number", required=False, )
    letter_date = fields.Date(string="Letter Date", required=False, )
    letter_details = fields.Text(string="Letter Details", required=False, )
    signature = fields.Many2one(comodel_name="hr.employee", string="signature", required=False, )
    @api.depends('origin')
    def get_sale_id(self):
        for rec in self:
            rec.sale_id = self.env['sale.order'].search([('name','=',rec.origin)])

class khasp_invoice_line_modification(models.Model):
    _inherit = 'account.invoice.line'
    unit_price_with_tax = fields.Float(string="",  compute='get_residual_fields', )
    total_price_with_tax = fields.Float(string="",  compute='get_residual_fields', )

    @api.depends('invoice_line_tax_ids','quantity','price_unit')
    def get_residual_fields(self):
        for rec in self:
            total_tax = 0
            for tax in rec.invoice_line_tax_ids:
                total_tax += tax.amount
            rec.total_price_with_tax = ((rec.price_unit * (total_tax / 100)) + rec.price_unit) * rec.quantity
            rec.unit_price_with_tax = (rec.price_unit * (total_tax / 100)) + rec.price_unit


