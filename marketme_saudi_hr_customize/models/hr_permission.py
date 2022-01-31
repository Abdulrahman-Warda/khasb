""" Initialize Hr Permission """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import date, datetime, time, timedelta


class HrPermission(models.Model):
    """
        Initialize Hr Permission:
         - 
    """
    _name = 'hr.permission'
    _description = 'Hr Permission'
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
    date_time_from = fields.Datetime(
        track_visibility='onchange'
    )
    date_time_to = fields.Datetime(
        track_visibility='onchange'
    )
    date_time_duration = fields.Float(
        compute='_compute_date_time_duration'
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
        return super(HrPermission, self).write(vals)

    def unlink(self):
        """ Override unlink """
        if self.state != 'draft':
            raise ValidationError('You can not delete in this stage !')
        return super(HrPermission, self).unlink()

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            permission_type = self.env['ir.config_parameter'].sudo().get_param('permission_type')
            permission_no = self.env['ir.config_parameter'].sudo().get_param('permission_no')
            if permission_type == 'no_limit':
                rec.write({
                    'state': 'confirm'
                })
                permission_leave = self.env.ref('marketme_saudi_hr_customize.hr_permission_leave')
                leave = self.env['hr.leave'].create({
                    'holiday_status_id': permission_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_time_from,
                    'request_unit_half': True,
                })
                leave.action_approve()
            elif permission_type == 'monthly':
                today = fields.Date.today()
                first_date = today.replace(day=1)
                last_date = today.replace(month=today.month+1, day=1)
                permissions = self.search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('date_time_from', '>=', first_date),
                    ('date_time_from', '<', last_date),
                             ])
                if int(permission_no) < len(permissions):
                    raise ValidationError('You use your possible permissions !')
                else:
                    rec.write({
                        'state': 'confirm'
                    })
                permission_leave = self.env.ref('marketme_saudi_hr_customize.hr_permission_leave')
                leave = self.env['hr.leave'].create({
                    'holiday_status_id': permission_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_time_from,
                    'request_unit_half': True,
                })
                leave.action_approve()
            elif permission_type == 'annual':
                today = fields.Date.today()
                first_date = today.replace(day=1, month=1)
                last_date = today.replace(day=31, month=12)
                permissions = self.search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('date_time_from', '>=', first_date),
                    ('date_time_from', '<', last_date),
                             ])
                if int(permission_no) < len(permissions):
                    raise ValidationError('You use your possible permissions !')
                else:
                    rec.write({
                        'state': 'confirm'
                    })
                permission_leave = self.env.ref('marketme_saudi_hr_customize.hr_permission_leave')
                leave = self.env['hr.leave'].create({
                    'holiday_status_id': permission_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_time_from,
                    'request_unit_half': True,
                })
                leave.action_approve()
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

    @api.depends('date_time_from', 'date_time_to')
    def _compute_date_time_duration(self):
        """ Compute duration value """
        for rec in self:
            if rec.date_time_from and rec.date_time_to:
                time_difference = rec.date_time_to - rec.date_time_from
                seconds = time_difference.total_seconds()
                rec.date_time_duration = seconds / 3600
            else:
                rec.date_time_duration = 0
