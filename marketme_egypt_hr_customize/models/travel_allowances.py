""" Initialize Travel Allowances """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class TravelAllowances(models.Model):
    """
        Initialize Travel Allowances:
         -
    """
    _name = 'travel.allowances'
    _description = 'Travel Allowances'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_available_employee_ids(self):
        if self.env.user.has_group('marketme_egypt_hr_customize.group_allowance_and_deduction_own_document'):
            available_employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        elif self.env.user.has_group('marketme_egypt_hr_customize.group_allowance_and_deduction_department_document'):
            available_employee_ids = self.env['hr.employee'].search([('parent_id.user_id', '=', self.env.user.id)])
        else:
            available_employee_ids = self.env['hr.employee'].search([])
        return available_employee_ids

    employee_id = fields.Many2one(
        'hr.employee',
        track_visibility='onchange'
    )
    available_employee_ids = fields.Many2many(
        'hr.employee',
        default=lambda s: s._get_available_employee_ids(),
    )
    date_from = fields.Date(
        track_visibility='onchange'
    )
    date_to = fields.Date(
        track_visibility='onchange'
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
    duration = fields.Integer(
        compute='_compute_duration'
    )
    travel_type = fields.Selection(
        [('internal', 'Internal'),
         ('abroad', 'Abroad'),
         ('other', 'Other')],
        default='internal',
        track_visibility='onchange'
    )
    travel_duration_type = fields.Selection(
        [('days', 'Days'),
         ('hours', 'Hours')],
        default='days',
        track_visibility='onchange'
    )
    amount = fields.Float(
        compute='_compute_amount'
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })
            travel_leave = self.env.ref('marketme_egypt_hr_customize.hr_travel_leave')
            if rec.travel_duration_type == 'days':
              leave = self.env['hr.leave'].create({
                    'holiday_status_id': travel_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_from,
                    'request_date_to': rec.date_to,
                    'number_of_days': rec.duration,
                })
              leave.action_approve()
            else:
              leave = self.env['hr.leave'].create({
                    'holiday_status_id': travel_leave.id,
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

    @api.depends('date_from', 'date_to')
    def _compute_duration(self):
        """ Compute duration value """
        for rec in self:
            if rec.date_from and rec.date_to:
                time_difference = relativedelta(rec.date_to, rec.date_from)
                rec.duration = time_difference.days + 1
            else:
                rec.duration = 0

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

    @api.depends('employee_id', 'duration', 'travel_type')
    def _compute_amount(self):
        """ Compute amount value """
        for rec in self:
            if rec.travel_duration_type == 'days':
                if rec.travel_type == 'internal':
                    if rec.employee_id.contract_id.internal_travel_allowances and rec.duration:
                        rec.amount = rec.duration * rec.employee_id.contract_id.internal_travel_allowances
                    else:
                        rec.amount = 0
                if rec.travel_type == 'abroad':
                    if rec.employee_id.contract_id.abroad_travel_allowances and rec.duration:
                        rec.amount = rec.duration * rec.employee_id.contract_id.abroad_travel_allowances
                    else:
                        rec.amount = 0
                if rec.travel_type == 'other':
                    if rec.employee_id.contract_id.other_travel_allowances and rec.duration:
                        rec.amount = rec.duration * rec.employee_id.contract_id.other_travel_allowances
                    else:
                        rec.amount = 0
            else:
                if rec.employee_id.contract_id.hour_travel_allowances and rec.date_time_duration:
                    rec.amount = rec.date_time_duration * rec.employee_id.contract_id.hour_travel_allowances
                else:
                    rec.amount = 0
