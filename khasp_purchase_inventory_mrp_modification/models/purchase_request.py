# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_purchase_request_modification(models.Model):
    _inherit = 'sprogroup.purchase.request'
    def get_done(self):
        for rec in self:
            rec.state ='done'