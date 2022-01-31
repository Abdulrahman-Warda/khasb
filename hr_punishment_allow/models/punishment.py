# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime




class Punishment(models.Model):
    _name='hr.punishment'

    _rec_name='employee_id'

    date = fields.Datetime(string="Date", required=True, default=datetime.now(),states={'confirm': [('readonly', True)]})
    type = fields.Selection(string="Type", selection=[('employee', 'Employee'), ('department', 'Department'), ], required=False,states={'confirm': [('readonly', True)]})
    employee_id = fields.Many2one('hr.employee', string='Employee', required=False,states={'confirm': [('readonly', True)]})
    department_id = fields.Many2one('hr.department', string='Department', required=False,states={'confirm': [('readonly', True)]})
    state = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ],required=False, default='draft',states={'confirm': [('readonly', True)]})
    amount = fields.Float(string="Amount", required=False,states={'confirm': [('readonly', True)]})

    @api.multi
    @api.constrains('employee_id', 'date','department_id')
    def _check_uniques_from_branch_with_to_branch(self):
        domain = []
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))

        if self.date:
            domain.append(('date', '=', str(self.date)))
        list = self.env['hr.punishment'].search(domain)
        if len(list) > 1:
            raise ValidationError("من فضلك لا تكرر")






    def confirm(self):
        self.state='confirm'





