""" Initialize Hr Permission """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import date, datetime, time, timedelta


class HrTransfer(models.Model):
    """
        Initialize Hr transfer:
         - 
    """
    _name = 'hr.transfer'
    _description = 'Hr transfer'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_available_employee_ids(self):
        if self.env.user.has_group('marketme_saudi_hr_customize.group_hr_own_document'):
            available_employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        elif self.env.user.has_group('marketme_saudi_hr_customize.group_hr_department_document'):
            available_employee_ids = self.env['hr.employee'].search([('parent_id.user_id', '=', self.env.user.id)])
        else:
            available_employee_ids = self.env['hr.employee'].search([])
        return available_employee_ids

    employee_id = fields.Many2one(
        'hr.employee',
        track_visibility='onchange',
        default=lambda self:self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1),
    )
    available_employee_ids = fields.Many2many(
        'hr.employee',
        default=lambda s: s._get_available_employee_ids(),
    )
    date = fields.Date(
        track_visibility='onchange'
    )
    new_job_id = fields.Many2one(
        'hr.job'
    )
    new_department_id = fields.Many2one(
        'hr.department'
    )

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )

    def write(self, vals):
        """ Override write """
        if self.state in ['confirm'] and not self.env.user.has_group('marketme_saudi_hr_customize.group_hr_all_document'):
            raise ValidationError('You can not edit in this stage !')
        return super(HrTransfer, self).write(vals)

    def unlink(self):
        """ Override unlink """
        if self.state != 'draft':
            raise ValidationError('You can not delete in this stage !')
        return super(HrTransfer, self).unlink()

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })
            rec.employee_id.update({
                'department_id': rec.new_department_id.id,
                'job_id': rec.new_job_id.id,
            })

    def action_cancel(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'cancel'
            })

    def action_draft(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'draft'
            })
