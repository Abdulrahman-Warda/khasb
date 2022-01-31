# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api
#
# class PurchaseInherit(models.Model):
#     _inherit = 'purchase.order'
#
#     # other_purchase = fields.Selection([('other_purchase', 'مصروفات أخرى')],string='مصروفات أخرى',default='other_purchase')
#     other_purchase = fields.Float('مصروفات أخرى')
#
#     state = fields.Selection(selection_add=[('accept', 'موافقة')])
#
#     def button_accept(self):
#         for rec in self:
#             rec.state = 'accept'
#
# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     other_purchase = fields.Float(string="مصروفات أخرى",related='order_id.other_purchase', store=True, readonly=False)
