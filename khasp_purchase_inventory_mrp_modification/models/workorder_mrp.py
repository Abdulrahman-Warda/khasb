# -*- coding: utf-8 -*-
from odoo import models, fields, api
class khasp_work_order_modification(models.Model):
    _inherit = 'mrp.workorder'

    worker_id = fields.Many2one(comodel_name="res.users", string="worker", required=False, )
    tool_id = fields.Many2one(comodel_name="product.template", string="Tool", required=False, domain=[('is_tool','=',True)])
    pause_history_ids = fields.One2many(comodel_name="workorder.pause", inverse_name="workorder_ref", string="Pause History", readonly=True)
    worker_ids = fields.Many2many(comodel_name="res.users", string="Workers", )

    done_loc_id = fields.Many2one(comodel_name="stock.location", string="Done Location", required=False)
    not_done_loc_id = fields.Many2one(comodel_name="stock.location", string="Not Done Location", required=False)
    qty_is_done = fields.Float(string="Quantityy Done", required=False)
    qty_not_done = fields.Float(string="Quantityy Not Done", required=False)
    qty_production = fields.Float('Original Production Quantity', readonly=True, related='production_id.product_qty',store=True)
    qty_next_done = fields.Float('Quantity Done',)


    

    @api.onchange('worker_ids')
    def get_workcenter(self):
        for rec in self:
            print("work_center",self.workcenter_id)
            order=self.env['mrp.workorder']
            print('order', order)
            workcenter_order = order.search([('workcenter_id', '=', rec.id)])
            print('workcenter_order', workcenter_order)


    @api.multi
    def record_production(self):
        res = super(khasp_work_order_modification, self).record_production()
        tool_id=self.env['workorder.tool'].create({
            'product_id':self.tool_id.id,
            'workorder_ref':self.id,
            'qty_produced':self.qty_produced,
        })
        tool_id.get_usage_number()

        for r in self:
            r.next_work_order_id.write({'qty_production':r.qty_produced,'qty_next_done':r.qty_next_done
                                        ,'done_loc_id':r.done_loc_id.id
                                        ,'not_done_loc_id':r.not_done_loc_id.id
                                        ,'qty_is_done':r.qty_is_done
                                        ,'qty_not_done':r.qty_not_done,
                                        })
        return res
