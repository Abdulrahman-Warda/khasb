# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseInherit(models.Model):
    _inherit = 'account.asset.asset'

    employee_name = fields.Many2one('hr.employee', string="Employee name")

    department_name = fields.Many2one('hr.department', string="Department name")
