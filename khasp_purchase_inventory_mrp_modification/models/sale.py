# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_sales_modification(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(khasp_sales_modification, self).action_confirm()
        for rec in self:
            stock = self.env['stock.picking'].search([('sale_id', '=', rec.id),('state', '=', 'assigned')])
            for s in stock:
                s.state='quality_control'

        return res