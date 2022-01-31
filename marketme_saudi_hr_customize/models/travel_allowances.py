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
    _description = 'Business Trip'
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
         ('approve', 'Approve'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )
    travel_from_id = fields.Many2one(
        'res.country',
    )
    travel_to_id = fields.Many2one(
        'res.country',
    )
    payslip = fields.Boolean()
    emp_account_id = fields.Many2one('account.account', string="Loan Account")
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })
            travel_leave = self.env.ref('marketme_saudi_hr_customize.hr_travel_leave')
            if rec.travel_duration_type == 'days':
              leave = self.env['hr.leave'].sudo().create({
                    'holiday_status_id': travel_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_from,
                    'request_date_to': rec.date_to,
                    'number_of_days': rec.duration,
                })
              leave.action_approve()
            else:
              leave = self.env['hr.leave'].sudo().create({
                    'holiday_status_id': travel_leave.id,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                    'request_date_from': rec.date_time_from,
                    'request_unit_half': True,
                })
              leave.action_approve()

    def action_accounting_approve(self):
        """ Action Accounting Approve """
        if not self.payslip:
            contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
            if not contract_obj:
                raise UserError('You must Define a contract for employee')
            else:
                if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
                    raise UserError("You must enter employee account & Treasury account and journal to approve ")
                for rec in self:
                    amount = rec.amount
                    travel_name = rec.employee_id.name
                    reference = rec.employee_id.name + ' Business Trip'
                    journal_id = rec.journal_id.id
                    debit_account_id = rec.treasury_account_id.id
                    credit_account_id = rec.emp_account_id.id
                    debit_vals = {
                        'name': travel_name,
                        'account_id': debit_account_id,
                        'journal_id': journal_id,
                        'partner_id': rec.employee_id.address_id.id or None,
                        'date': fields.Date.today(),
                        'debit': amount > 0.0 and amount or 0.0,
                        'credit': amount < 0.0 and -amount or 0.0,
                    }
                    credit_vals = {
                        'name': travel_name,
                        'account_id': credit_account_id,
                        'journal_id': journal_id,
                        'partner_id': rec.employee_id.address_id.id or None,
                        'date': fields.Date.today(),
                        'debit': amount < 0.0 and -amount or 0.0,
                        'credit': amount > 0.0 and amount or 0.0,
                    }
                    vals = {
                        'name': 'Business Trip For' + ' ' + travel_name,
                        'narration': travel_name,
                        'ref': reference,
                        'journal_id': journal_id,
                        'partner_id': rec.employee_id.address_id.id or None,
                        'date': fields.Date.today(),
                        'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                    }
                    move = self.env['account.move'].create(vals)
                    move.post()
        self.write({'state': 'confirm'})
        return True

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
