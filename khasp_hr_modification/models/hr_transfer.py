# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning

class khasp_hr_transfer_modification(models.Model):
    _inherit = 'hr.transfer'
    state = fields.Selection(
        [('draft', 'Employee'),
         ('direct_manger', 'Direct Manger'),
         ('department_manger', 'New Department Manger'),
         ('general_manger', 'General Manger'),
         ('hr_manger', 'HR Manger'),
         ('confirm', 'Confirm'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )
    def action_employee(self):
        for rec in self:
            rec.state = 'direct_manger'
    def action_direct_manger(self):
        for rec in self:
            current_user = self.env.uid
            if current_user != rec.employee_id.parent_id.user_id.id:
                raise ValidationError("you can\'t approve this request")
            rec.state = 'department_manger'
    def action_department_manger(self):
        for rec in self:
            current_user = self.env.uid
            if current_user != rec.new_department_id.manager_id.id:
                raise ValidationError("you can\'t approve this request")
            rec.state = 'general_manger'
    def action_general_manger(self):
        for rec in self:
            rec.state = 'hr_manger'
    def action_hr_manger(self):
        for rec in self:
            rec.state = 'confirm'


