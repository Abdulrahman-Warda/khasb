# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float('Discount')
    discountSelect = fields.Selection([('percentage', '%'), ('value', 'Value')],string='Discount Type')
    other_purchase = fields.Float(string="Other expenses", related='order_id.other_purchase', store=True, readonly=False)


    @api.depends('product_qty', 'price_unit', 'taxes_id','discount','other_purchase','discountSelect')
    def _compute_amount(self):
        for line in self:
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            if line.discount:
                if line.discountSelect == 'percentage':
                    discount = (line.price_unit * line.discount * line.product_qty)/100
                    line.update({
                        'price_tax': taxes['total_included'] - taxes['total_excluded'],
                        'price_total': taxes['total_included'],
                        'price_subtotal': taxes['total_excluded'] - discount + line.other_purchase,
                    })
                elif line.discountSelect == 'value':
                    line.update({
                        'price_tax': taxes['total_included'] - taxes['total_excluded'],
                        'price_total': taxes['total_included'],
                        'price_subtotal': taxes['total_excluded'] - line.discount + line.other_purchase,
                    })
                    print(line.discount)
            else:
                line.update({
                    'price_tax': taxes['total_included'] - taxes['total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'] + line.other_purchase,
                })


class PurchaseInherit(models.Model):
    _inherit = 'purchase.order'

    other_purchase = fields.Float('Other expenses')

    # state = fields.Selection(selection_add=[('accept', 'موافقة')])

    def button_accept(self):
        for rec in self:
            rec.state = 'accept'

