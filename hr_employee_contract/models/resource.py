# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"


    holiday_mission_type = fields.Boolean(string="Is Mission", default=False)

    holiday_sick_leave_type = fields.Boolean(string="Is Sick", default=False)

    time_type = fields.Selection([('leave', 'Leave'), ('other', 'Other')])
