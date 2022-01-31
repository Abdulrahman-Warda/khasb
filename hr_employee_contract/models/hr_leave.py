# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, timedelta, date


class HrLeave(models.Model):
    _inherit = "hr.leave"

    in_out_capital = fields.Selection(related='holiday_status_id.in_out_capital', string='In / Out Capital')
    holiday_status_mission = fields.Boolean(related='holiday_status_id.holiday_mission_type', store=True)
    holiday_status_sick = fields.Boolean(related='holiday_status_id.holiday_sick_leave_type', store=True)
    allowance_amount = fields.Float()
    deduction_sick_amount = fields.Float(string="Deduction Sick Amount")

    @api.onchange('holiday_status_mission', 'in_out_capital', 'request_unit_half',
                  'request_date_from', 'request_date_to', 'holiday_status_sick')
    def onchange_leave_types_mission_and_sick(self):
        if self.holiday_status_mission == True and not self.request_unit_half:
            if self.leave_type_request_unit == 'day':
                if self.number_of_days <= 3:
                    if self.in_out_capital == 'in_cairo':
                        self.allowance_amount = 50 * self.number_of_days
                    elif self.in_out_capital == 'out_cairo':
                        self.allowance_amount = 100 * self.number_of_days
                else:
                    if self.employee_id.employee_work_type == 'office' and self.employee_id.contract_id:
                        employee_wage = self.employee_id.contract_id.wage
                        the_day_wage = employee_wage / 22
                        if employee_wage < 3000:
                            self.allowance_amount = the_day_wage * (50 / 100) * self.number_of_days
                        elif employee_wage >= 3000 and employee_wage <= 4500:
                            self.allowance_amount = the_day_wage * (40 / 100) * self.number_of_days
                        elif employee_wage > 4500 and employee_wage <= 7000:
                            self.allowance_amount = the_day_wage * (30 / 100) * self.number_of_days
                        elif employee_wage > 7000:
                            self.allowance_amount = the_day_wage * (25 / 100) * self.number_of_days
                    elif self.employee_id.employee_work_type == 'site' and self.employee_id.contract_id:
                        employee_wage = self.employee_id.contract_id.wage
                        the_day_wage = employee_wage / 26
                        if employee_wage < 3000:
                            self.allowance_amount = the_day_wage * (50 / 100) * self.number_of_days
                        elif employee_wage >= 3000 and employee_wage <= 4500:
                            self.allowance_amount = the_day_wage * (40 / 100) * self.number_of_days
                        elif employee_wage > 4500 and employee_wage <= 7000:
                            self.allowance_amount = the_day_wage * (30 / 100) * self.number_of_days
                        elif employee_wage > 7000:
                            self.allowance_amount = the_day_wage * (25 / 100) * self.number_of_days
                    else:
                        self.allowance_amount = 0
            else:
                self.allowance_amount = 0
        else:
            self.allowance_amount = 0

        # TODO check the leave type is sick and deduction quarter_day_value * days of leave and add to field in form
        if self.holiday_status_sick == True:
            print("ahmed saber")
            quarter_day_value = self.employee_id.contract_id.wage / 30 * (25 / 100)
            print("quarter_day", quarter_day_value)
            print("quarter_day", self.number_of_days_display)
            self.deduction_sick_amount = quarter_day_value * self.number_of_days_display
        else:
            self.deduction_sick_amount = 0
