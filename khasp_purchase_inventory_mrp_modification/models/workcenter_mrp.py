# -*- coding: utf-8 -*-
from odoo import models, fields, api
class khasp_work_center_modification(models.Model):
    _inherit = 'mrp.workcenter'

    worker_ids = fields.Many2many(comodel_name="res.users", string="Workers", )
    workers_ids = fields.Many2many(comodel_name="res.users", relation="workcenter_user_relat",
                                   column1="workcenter_id", column2="user_id", string="Workers", )

    @api.onchange('worker_ids')
    def move_workers(self):
        print("hello world")
        order_list=[]
        workers=[]

        for rec in self:
            work_order = self.env['mrp.workorder'].sudo().search([('workcenter_id','=',rec.id)])
            print("work_order", work_order)
            # for order in work_order:
            #     if order.workcenter_id == rec.id:
            #         order_list.append(order)
            # print('order_list',order_list)
            # for worker in rec.worker_ids:
            #     workers.append(worker.id))
            #
            # for order in work_order:
            #     order.write({
            #         'worker_ids': [(6,0,workers)],
            #     })