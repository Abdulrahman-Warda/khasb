# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LeaveType(models.Model):
    _inherit='hr.leave.type'
    annual = fields.Boolean(string="سنوية")



