# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning

class khasp_hr_overtime_modification(models.Model):
    _inherit = 'hr.overtime'
    state = fields.Selection(
        [('draft', 'Employee'),
         ('direct_manger', 'Direct Manger'),
         ('hr_manger', 'HR Manger'),
         ('confirm', 'Confirm'),
         ('done', 'Done'),
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
            rec.state = 'hr_manger'


    def action_accounting_approve(self):
        res = super(khasp_hr_overtime_modification, self).action_accounting_approve()
        self.state = 'done'
        return res
