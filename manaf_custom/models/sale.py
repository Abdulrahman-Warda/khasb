from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def change_qty_bom(self):
        action = self.env.ref('manaf_custom.sale_bom_action').read()[0]
        bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)], limit=1)
        lines = []
        for line in bom.bom_line_ids:
            lines.append((0, 0,
                          {'product_id': line.product_id.id,
                           'qty': line.product_qty,
                           'bom_line_id': line.id}
                          ))

        vals = {'bom_id': bom.id,
                'product_id': self.product_id.id,
                'line_ids': lines}

        wiz_id = self.env['sale.bom'].create(vals)
        action['res_id']=wiz_id.id
        action['domain']=[('id','=',wiz_id)]
        return action

