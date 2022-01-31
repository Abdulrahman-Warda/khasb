# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import date,datetime

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'

    account_analytic = fields.Many2one('account.analytic.account', string='Analytic Account')

    # @api.multi
    # @api.onchange('account_analytic')
    # def _prepare_account_move_line(self):
    #     res = ({
    #         'analytic_account_id': self.account_analytic.id,
    #         'name':'',
    #         'product_id': False
    #     })
    #     self.env['stock.move'].create(res)
    #     print(res)
    #     return res

    # sale_preparation = {
    #     'partner_id': rec.partner_id.id,
    #     'partner_invoice_id': rec.partner_id.id,
    #     'partner_shipping_id': rec.partner_id.id,
    #     "default_start_date": rec.start_date,
    #     "default_end_date": rec.end_date,
    #     "payment_term_id": rec.payment_term_id.id,
    #     "contract_type": rec.contract_type,
    #     "order_line": contract_line,
    #     "tender_date": rec.tender_date,
    #     "tender_duration": rec.tender_duration,
    #     "guarantee_duration": rec.guarantee_duration,
    #     "connection_duration": rec.connection_duration,
    #     "payment_methode": rec.payment_methode,
    #     "maintenance": rec.maintenance,
    #     "notes": rec.notes,
    # }



    # @api.model
    # @api.onchange('account_analytic')
    # def _get_analytic_account(self):
    #     # count_id = self.env['stock.warehouse'].browse(self._context.get("active_id"))
    #     self.env['stock.move'].search([('warehouse_id', '=', self.id)]).update(
    #         {"analytic_account_id": self.account_analytic.id})
    #     # count = self.env.cr.execute("UPDATE stock.move SET analytic_account_id=%s WHERE warehouse_id=%s" % (r.account_analytic,count_id))
    #     # count = self.env['stock.move'].search_count([('picking_id', '=', r.picking_id)])
    #     # count = self.env['stock.picking'].search_count([('picking_id', '=', r.picking_id)])
    #     # self.env['stock.picking'].update({"analytic_account_id": r.account_analytic.id})
    #     print(self.account_analytic)

    # @api.model
    # def _get_analytic_account(self):
    #     for r in self:
    #         count = r.env.cr.execute("UPDATE stock.move SET analytic_account_id=%s ", + [tuple(r.account_analytic.id)])
    #         print(count)

    # @api.model
    # # @api.onchange('account_analytic')
    # def create(self, values):
    #     res = super(StockWarehouseInherit, self).create(values)
    #     # creating record in another model
    #     if values.get('account_analytic'):
    #         account_analytic_val = {
    #             'custom_account_analytic': values['account_analytic']
    #         }
    #         self.env['stock.picking'].create(account_analytic_val)
    #         print(res)
    #     return res

    # orders = self.env['sale.order'].browse(self._context.get("active_ids"))
    # for order in orders:
    #     self.env['sale.order.line'].search([('order_id', '=', order.id)]).update({"price_unit": self.new_price})

    # @api.multi
    # @api.onchange('account_analytic')
    # def _get_analytic_account(self):
    #     for r in self:
    #         count = r.env.cr.execute("UPDATE stock.move SET analytic_account_id=%s ", + [tuple(r.account_analytic.id)])
    #         print(count)

    # warehouse_id


