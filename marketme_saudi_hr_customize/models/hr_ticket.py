""" Initialize Hr Permission """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import date, datetime, time, timedelta


class HrTicket(models.Model):
    """
        Initialize Hr ticket:
         - 
    """
    _name = 'hr.ticket'
    _description = 'Hr Ticket'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_available_employee_ids(self):
        if self.env.user.has_group('marketme_saudi_hr_customize.group_hr_own_document'):
            available_employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.user.id),
                                                                     ('country_id', '!=', self.env.ref('base.sa').id)])
        elif self.env.user.has_group('marketme_saudi_hr_customize.group_hr_department_document'):
            available_employee_ids = self.env['hr.employee'].search([('parent_id.user_id', '=', self.env.user.id),
                                                                     ('country_id', '!=', self.env.ref('base.sa').id)])
        else:
            available_employee_ids = self.env['hr.employee'].search([('country_id', '!=', self.env.ref('base.sa').id)])
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
    ticket_day = fields.Date(
        track_visibility='onchange'
    )
    destination_id = fields.Many2one(
        'res.country',
        track_visibility='onchange'
    )
    ticket_cost = fields.Float(
        track_visibility='onchange'
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
    emp_account_id = fields.Many2one('account.account', string="Loan Account")
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")

    def write(self, vals):
        """ Override write """
        if self.state in ['confirm'] and not self.env.user.has_group('marketme_saudi_hr_customize.group_hr_all_document'):
            raise ValidationError('You can not edit in this stage !')
        return super(HrTicket, self).write(vals)

    def unlink(self):
        """ Override unlink """
        if self.state != 'draft':
            raise ValidationError('You can not delete in this stage !')
        return super(HrTicket, self).unlink()

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })
            
    def action_accounting_approve(self):
        """ Action Accounting Approve """
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise UserError('You must Define a contract for employee')
        else:
            if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError("You must enter employee account & Treasury account and journal to approve ")
            for rec in self:
                amount = rec.ticket_cost
                ticket_name = rec.employee_id.name
                reference = rec.employee_id.name + ' Ticket'
                journal_id = rec.journal_id.id
                debit_account_id = rec.treasury_account_id.id
                credit_account_id = rec.emp_account_id.id
                debit_vals = {
                    'name': ticket_name,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'partner_id': rec.employee_id.address_id.id or None,
                    'date': fields.Date.today(),
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                }
                credit_vals = {
                    'name': ticket_name,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'partner_id': rec.employee_id.address_id.id or None,
                    'date': fields.Date.today(),
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                }
                vals = {
                    'name': 'Ticket For' + ' ' + ticket_name,
                    'narration': ticket_name,
                    'partner_id': rec.employee_id.address_id.id or None,
                    'ref': reference,
                    'journal_id': journal_id,
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
