# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
class khasp_workorder_pause_modification(models.Model):
    _name = 'workorder.tool'

    product_id = fields.Many2one(comodel_name="product.template", string="Product", required=False, )
    workorder_ref = fields.Many2one(comodel_name="mrp.workorder", string="Work Order ID")
    qty_produced = fields.Float(string="Number Of Finished Products",  required=False, )
    factory_manger = fields.Many2one(comodel_name="res.users", string="Factory Manger", required=False, )

    def get_usage_number(self):
        for rec in self:
            number=self.env['workorder.tool'].search_count([('product_id','=',rec.product_id.id)])
            print("number",number,rec.product_id.name)
            if number > 1:
                print("more than the minimum")
                # rec.factory_manger = self.env['res.users'].search([('is_factory_manger','=',True)],limit=1)
                email_temp=self.env.ref('khasp_purchase_inventory_mrp_modification.tool_expiration_mail').id
                print('email_temp',email_temp)
                temp = self.env['mail.template'].browse(email_temp)
                print('temp',temp)
                # temp.send_mail(self.id, force_send=force_send)
