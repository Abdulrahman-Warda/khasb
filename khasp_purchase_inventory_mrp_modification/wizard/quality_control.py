# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_quality_control_modification(models.TransientModel):
    _name = 'quality.control.inventory.wizard'
    def get_stock_ref(self):
        return self.env['stock.picking'].browse(self._context.get('active_id'))

    def get_lines(self):
        lines=[]
        pick=self.env['stock.picking'].browse(self._context.get('active_id'))
        for move in pick.move_ids_without_package:
            lines.append((0,0,{
                'move_id':move.id,
                'product_id':move.product_id.id
            }))
        return lines


    stock_ref = fields.Many2one(comodel_name="stock.picking", string="Stock ID", default=get_stock_ref, )
    qc_pass = fields.Boolean(string="Pass",  )
    qc_fail = fields.Boolean(string="Fail",  )
    qc_state = fields.Selection(string="State", selection=[('pass', 'Pass'), ('fail', 'Fail'), ], required=False, )
    lines = fields.One2many(comodel_name="qlity.st.lines", inverse_name="wiz_id", string="", required=False,default=get_lines)


    def quality_control_pass(self):
        for rec in self:
            if rec.qc_state == 'pass':
                rec.stock_ref.write({'state':'assigned'})
                rec.stock_ref.state = 'assigned'
                for line in rec.lines:
                    print("LLLLLLLLLLL")
                    line.move_id.sudo().write({'quantity_done':line.qty})
            elif rec.qc_state == 'fail':
                rec.stock_ref.write({'state':'qc_rejection'})
                for line in rec.lines:
                    print(">>>>>>>>>>>>>")
                    line.move_id.sudo().write({'quantity_done': line.move_id.product_uom_qty-line.qty})
            return rec.stock_ref.button_validate()




class WizardLine(models.TransientModel):
    _name='qlity.st.lines'
    move_id = fields.Many2one(comodel_name="stock.move", string="", required=False)
    product_id = fields.Many2one(comodel_name="product.product", string="product", required=False)
    qty = fields.Integer(string="quantity", required=False)
    wiz_id = fields.Many2one(comodel_name="quality.control.inventory.wizard")
