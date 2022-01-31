# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class EmployeesTermination(models.Model):
    _name = 'hr.termination'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=False, readonly=True)
    state = fields.Selection([
        ('hr_officer', 'HR Officer'),
        ('hr_manager', 'HR Manager'),
        ('financial_manager', 'Financial Manager'),
        ('general_manager', 'General Manager'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, default='hr_officer')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    company_id = fields.Many2one('res.company', readonly=True, related='employee_id.company_id')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    joining_date = fields.Date(readonly=True, related='contract_id.date_start')
    notes = fields.Text(string="", required=False, )

    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('hr.termination.sequence')) or 'New'
        return super(EmployeesTermination, self).create(vals)

    def hr_officer_approval(self):
        self.state = 'hr_manager'

    def hr_manager_approval(self):
        self.state = 'financial_manager'

    def financial_manager_approval(self):
        self.state = 'general_manager'

    def general_manager_approval(self):
        self.state = 'approved'
    def reject(self):
        self.state = 'rejected'
