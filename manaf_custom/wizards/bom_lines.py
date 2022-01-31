from odoo import api, fields, models
from odoo.exceptions import ValidationError




class Bom(models.TransientModel):
    _name='sale.bom'
    line_ids = fields.One2many(comodel_name="sale.bom.line", inverse_name="wiz_id", string="Lines", required=False)
    bom_id = fields.Many2one(comodel_name="mrp.bom", string="Bill of Materials", readonly=True)
    product_id = fields.Many2one(comodel_name="product.product", string="Product", readonly=True)

    def change_qty(self):
        for line in self.line_ids:
            if line.bom_line_id:
                line.bom_line_id.sudo().write({'product_qty':line.qty})
            else:
                self.env['mrp.bom.line'].create({
                    'product_id':line.product_id.id,
                    'product_qty':line.qty,
                    'bom_id':self.bom_id.id,
                })




class Bom(models.TransientModel):
    _name='sale.bom.line'

    wiz_id = fields.Many2one(comodel_name="sale.bom")
    bom_line_id = fields.Many2one(comodel_name="mrp.bom.line")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", readonly=False)
    qty = fields.Float(string="Quantity", required=False)



