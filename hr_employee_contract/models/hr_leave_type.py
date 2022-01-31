# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    holiday_mission_type = fields.Boolean(string="Is Mission", default=False)

    holiday_sick_leave_type = fields.Boolean(string="Is Sick", default=False)

    time_type = fields.Selection([('leave', 'Leave'), ('other', 'Other')])

    in_out_capital = fields.Selection([('in_cairo', 'In Cairo'), ('out_cairo', 'Out Cairo')], string='In / Out Capital')

