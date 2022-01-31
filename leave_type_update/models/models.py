# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeaveTypeInherit(models.Model):
    _inherit = 'hr.leave.type'

    max_days = fields.Integer(string="Maximum Days", required=False, )
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ], required=False, )

    leave_type = fields.Selection(string="", selection=[('marriage', 'Marriage Leave'), ('Hajj', 'Hajj Leave'),
                                                        ('exams', 'Exams Leave'),
                                                        ('maternity', 'Maternity leave'), ('death', 'Death Leave'),
                                                        ('divorce', 'Divorce Leave'),
                                                        ('newborn', 'Newborn Leave'), ('paid', 'Paid Leave'),
                                                        ('unpaid', 'Unpaid Leave'),
                                                        ('business_trip', 'Business Trip Leave'),
                                                        ('sick', 'Sick Leave'), ('permission', 'Permission Leave'),
                                                        ('legal', 'Legal Leave')],
                                  required=False, )

    alternative_employee = fields.Boolean(string="Alternative Employee ?", )
    accrual_allocation = fields.Boolean()
    accrual_allocation_count = fields.Float()
    def _cron_accrual_allocation(self):
        for leave_type in self.env['hr.leave.type'].search([('accrual_allocation','=',True)]):
            if leave_type.accrual_allocation_count > 0:
                for contract in self.env['hr.contract'].search([('eligible_for_accrual_allocation','=',True),('company_id','=',leave_type.company_id.id)]):
                    accrual_allocation = self.env['hr.leave.allocation'].create({
                        'employee_id':contract.employee_id.id,
                        'holiday_status_id':leave_type.id,
                        'number_of_days':leave_type.accrual_allocation_count,
                        'number_of_days_display':leave_type.accrual_allocation_count,
                        'holiday_type':'employee',
                        'name':contract.employee_id.name + " - Accrual - " + str(fields.Date.today()),
                        'state': 'validate'
                        })
class LeaveType(models.Model):
    _inherit = 'hr.leave'

    if_alternative_employee = fields.Boolean(string="If Alternative Employee ?",
                                             related="holiday_status_id.alternative_employee")

    alternative_employee = fields.Many2one(comodel_name="hr.employee", string="Alternative Employee", required=False, )

class Contract(models.Model):
    _inherit = 'hr.contract'

    eligible_for_accrual_allocation = fields.Boolean()
