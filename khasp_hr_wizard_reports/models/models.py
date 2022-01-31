# -*- coding: utf-8 -*-

from odoo import models, fields, api

class khasp_hr_employee_edit(models.Model):
    _inherit='hr.employee'
    joining_date = fields.Date(string="Joining Date", required=False, )
