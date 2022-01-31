# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_product_modification(models.Model):
    _inherit = 'product.template'
    workorder_ids = fields.One2many(comodel_name="workorder.tool", inverse_name="product_id",
                                    string="Work Orders", required=False, )
    is_tool = fields.Boolean(string="Is Tool",  )
    def unlink_workorders(self):
        for rec in self:
            tools = self.env['workorder.tool'].search([('product_id','=',rec.id)])
            for tool in tools:
                tool.unlink()