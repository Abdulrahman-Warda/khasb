# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Scrap(models.Model):
    _inherit='stock.scrap'
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False)
    scrap_tags = fields.Many2many(comodel_name="scrap.tag", relation="sc_tags",string="Tags")


    def create_so(self):
        vals = self._prepare_sale_order_vals()
        vals['order_line']=[(0,0,self._prepare_sale_order_line_vals())]
        print(">>", vals)
        order = self.env['sale.order'].create(vals)
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['domain']=[('id','=',order.id)]
        return action



    def _prepare_sale_order_line_vals(self):
        vals = {
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'price_unit': self.product_id.list_price,
            'product_uom_qty': self.scrap_qty,
        }
        return vals


    def _prepare_sale_order_vals(self):
        print(">>",self.scrap_location_id.name)
        print(">>",self.location_id.name)
        return {
            'origin': self.name,
            'partner_id': self.partner_id.id,
            'warehouse_id': self.env['stock.warehouse'].search([('lot_stock_id', '=', self.location_id.id)], limit=1).id
,

        }
class Scrap(models.Model):
    _name='scrap.tag'
    name = fields.Char(string="Name", required=True)
