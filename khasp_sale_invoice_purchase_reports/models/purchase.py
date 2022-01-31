# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_purchase_modification(models.Model):
    _inherit = 'purchase.order'
    delivery_within = fields.Integer(string="Delivery Within Days", required=False, )
    purchase_department = fields.Many2one(comodel_name="hr.employee", string="Purchase Dep.", required=False, )
    concerned_department = fields.Many2one(comodel_name="hr.employee", string="concerned Dep.", required=False, )
    general_manger = fields.Many2one(comodel_name="hr.employee", string="General Manger", required=False, )

    total_with_nothing = fields.Float(string="",  compute='get_total_fields', )
    total_discount = fields.Float(string="",  compute='get_total_fields', )

    @api.depends('order_line')
    def get_total_fields(self):
        total_with_nothing=0
        total_discount=0
        for rec in self:
            for line in rec.order_line:
                total_discount+=line.discount
                total_with_nothing+=(line.price_unit*line.product_qty)
            rec.total_with_nothing=total_with_nothing
            rec.total_discount=total_discount
            print("total_with_nothing",rec.total_with_nothing)
            print("total_discount",rec.total_discount)