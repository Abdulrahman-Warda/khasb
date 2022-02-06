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
    reason = fields.Text()


    def quality_control_pass(self):
        for rec in self:
            if len(rec.reason) > 0:
                rec.stock_ref.message_post(body=rec.reason)
                rec.stock_ref.note=rec.reason
            if rec.qc_state == 'pass':
                rec.stock_ref.write({'state':'assigned'})
                rec.stock_ref.state = 'assigned'
                for line in rec.lines:
                    if line.product_id.tracking != 'none':
                        if line.product_id.tracking == 'serial':
                            mls = line.move_id.move_line_ids.sorted(lambda i:i.id)
                            count=0
                            for ml in mls:
                                if count == line.qty:
                                    print(ml)
                                    ml.unlink()
                                else:
                                    count += 1
                            if line.move_id.product_uom_qty != line.qty:
                                line.move_id.sudo().write({'product_uom_qty': line.qty})
                        elif line.product_id.tracking == 'lot':
                            line.move_id.move_line_ids.qty_done = line.qty
                            if line.move_id.product_uom_qty != line.qty:
                                line.move_id.sudo().write({'product_uom_qty': line.qty})
                    else:
                        line.move_id.sudo().write({'quantity_done':line.qty})
                return rec.stock_ref.button_validate()
            elif rec.qc_state == 'fail':
                rec.stock_ref.write({'state':'qc_rejection'})
                for line in rec.lines:
                    if line.product_id.tracking != 'none':
                        if line.product_id.tracking == 'serial':
                            mls = line.move_id.move_line_ids.sorted(lambda i:i.id)
                            count=0
                            for ml in mls:
                                if count == line.move_id.product_uom_qty-line.qty:
                                    ml.unlink()
                                else:
                                    count += 1
                        elif line.product_id.tracking == 'lot':
                            line.move_id.move_line_ids.qty_done = line.move_id.move_line_ids.product_uom_qty-line.qty
                        if line.move_id.product_uom_qty != line.qty:
                            line.move_id.sudo().write({'product_uom_qty': line.move_id.product_uom_qty-line.qty})
                        else:
                            pass
                    else:
                        line.move_id.sudo().write({'quantity_done': line.move_id.product_uom_qty-line.qty})
                return rec.stock_ref.action_cancel()




class WizardLine(models.TransientModel):
    _name='qlity.st.lines'
    move_id = fields.Many2one(comodel_name="stock.move", string="", required=False)
    product_id = fields.Many2one(comodel_name="product.product", string="product", required=False)
    qty = fields.Integer(string="quantity", required=False)
    wiz_id = fields.Many2one(comodel_name="quality.control.inventory.wizard")
