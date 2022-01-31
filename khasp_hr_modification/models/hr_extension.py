# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning

class khasp_hr_handover_modification(models.Model):
    _inherit = 'hr.extension'
    state = fields.Selection(
        [('draft', 'Employee'),
         ('direct_manger', 'Direct Manger'),
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
            rec.state = 'hr_manger'
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    def set_draft(self):
        for rec in self:
            rec.state = 'draft'
    def action_hr_manger(self):
        for rec in self:
            if rec.contract_id:
                rec.contract_id.trial_date_end = rec.new_start_date
            else:
                raise ValidationError("you must make contract for this employee first")
            rec.state = 'confirm'


