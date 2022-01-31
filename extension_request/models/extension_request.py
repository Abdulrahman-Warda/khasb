# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class EmployeesExtension(models.Model):
    _name = 'hr.extension'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=False, readonly=True)
    state = fields.Selection([
        ('hr_officer', 'HR Officer'),
        ('d_manager', 'Direct Manager'),
        ('hr_manager', 'HR Manager'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, default='hr_officer')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    company_id = fields.Many2one('res.company', readonly=True, related='employee_id.company_id')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    joining_date = fields.Date(readonly=True, related='contract_id.date_start')
    trial_date_end = fields.Date(readonly=True, related='contract_id.trial_date_end')
    new_start_date = fields.Date(string="New End of Trial Period", readonly=False,)
    notes = fields.Text(string="", required=False, )

    score = fields.Float(string="Score",  required=False, )

    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('hr.extension.sequence')) or 'New'
        return super(EmployeesExtension, self).create(vals)

    def hr_officer_approval(self):
        self.state = 'd_manager'

    def d_manager_approval(self):
        self.state = 'hr_manager'

    def hr_manager_approval(self):
        self.contract_id.trial_date_end = self.new_start_date
        self.state = 'approved'

    def reject(self):
        self.state = 'rejected'
