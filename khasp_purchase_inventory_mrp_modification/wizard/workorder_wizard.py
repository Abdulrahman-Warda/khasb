# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
class khasp_quality_control_modification(models.TransientModel):
    _name = 'work.order.pause.wizard'

    def get_workorder_ref(self):
        return self.env['mrp.workorder'].browse(self._context.get('active_id'))

    workorder_ref = fields.Many2one(comodel_name="mrp.workorder", string="Work Order ID", default=get_workorder_ref, )
    pause_reason = fields.Selection(string="Pause Reason",
                            selection=[('rest', 'Rest'), ('partial', 'Partial Stop'), ], required=True, default='rest')
    products_no = fields.Integer(string="Number of finished Products", required=False, )
    reason = fields.Text(string="Reason", required=False, )

    def workorder_pause_confirm(self):
        for rec in self:
            if rec.pause_reason == 'rest':
                rec.workorder_ref.button_pending()
            elif rec.pause_reason == 'partial':
                if not rec.reason:
                    raise ValidationError(_('You must insert reason of pause process'))
                else:
                    self.env['workorder.pause'].create({
                        'workorder_ref':rec.workorder_ref.id,
                        'products_no':rec.products_no,
                        'reason':rec.reason,
                    })
                    # rec.workorder_ref.qty_produced += rec.products_no
                    rec.workorder_ref.button_pending()




class MakeDone(models.TransientModel):
    _name = 'work.order.done.wizard'

    def get_workorder_ref(self):
        return self.env['mrp.workorder'].browse(self._context.get('active_id'))

    workorder_ref = fields.Many2one(comodel_name="mrp.workorder", string="Work Order ID", default=get_workorder_ref, )
    qty_done = fields.Integer(string="Quantity Done", required=False)

    def workorder_done_confirm(self):
        for rec in self:
            if self.qty_done>rec.workorder_ref.qty_production:
                raise ValidationError("Quantity Done Must Less Than Quantity Producing")
            rec.workorder_ref.qty_producing =self.qty_done
            rec.workorder_ref.qty_next_done =self.qty_done
            rec.workorder_ref.qty_is_done =self.qty_done
            rec.workorder_ref.record_production()

