# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Department(models.Model):
    _inherit = 'hr.department'

    is_hr_department = fields.Boolean()
