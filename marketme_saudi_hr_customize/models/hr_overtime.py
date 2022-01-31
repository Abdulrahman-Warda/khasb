""" Initialize Hr Overtime """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrOvertime(models.Model):
    """
        Initialize Hr Overtime:
         - 
    """
    _name = 'hr.overtime'
    _description = 'Hr Overtime'
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
    request_date = fields.Date(
        track_visibility='onchange'
    )
    overtime_date = fields.Date(
        track_visibility='onchange'
    )
    overtime_hours = fields.Float()
    overtime_amount = fields.Float(
        compute='_compute_overtime_amount'
    )
    task = fields.Text()
    payslip = fields.Boolean()
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'),
         ('approve', 'Approve'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )
    day_type = fields.Selection(
        [('regular', 'Regular'),
         ('leave', 'leave')],
        default='regular',
    )

    emp_account_id = fields.Many2one('account.account', string="Loan Account")
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")

    @api.depends('overtime_hours', 'day_type', 'employee_id')
    def _compute_overtime_amount(self):
        """ Compute overtime_amount value """
        for rec in self:
            regular_day_rate = self.env['ir.config_parameter'].sudo().get_param('regular_day_rate')
            leave_day_rate = self.env['ir.config_parameter'].sudo().get_param('leave_day_rate')
            if rec.day_type == 'regular' and regular_day_rate:
                rec.overtime_amount = rec.overtime_hours * float(regular_day_rate) * rec.employee_id.contract_id.hour_rate
            elif rec.day_type == 'leave' and leave_day_rate:
                rec.overtime_amount = rec.overtime_hours * float(leave_day_rate) * rec.employee_id.contract_id.hour_rate
            else:
                rec.overtime_amount = 0

    def write(self, vals):
        """ Override write """
        if self.state in ['approve'] and not self.env.user.has_group('marketme_saudi_hr_customize.group_hr_all_document'):
            raise ValidationError('You can not edit in this stage !')
        return super(HrOvertime, self).write(vals)

    def unlink(self):
        """ Override unlink """
        if self.state != 'draft':
            raise ValidationError('You can not delete in this stage !')
        return super(HrOvertime, self).unlink()

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })

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
                    amount = rec.overtime_amount
                    over_name = rec.employee_id.name
                    reference = rec.employee_id.name + ' Overtime'
                    journal_id = rec.journal_id.id
                    debit_account_id = rec.treasury_account_id.id
                    credit_account_id = rec.emp_account_id.id
                    debit_vals = {
                        'name': over_name,
                        'account_id': debit_account_id,
                        'journal_id': journal_id,
                        'date': fields.Date.today(),
                        'partner_id': rec.employee_id.address_id.id or None,
                        'debit': amount > 0.0 and amount or 0.0,
                        'credit': amount < 0.0 and -amount or 0.0,
                    }
                    credit_vals = {
                        'name': over_name,
                        'account_id': credit_account_id,
                        'journal_id': journal_id,
                        'date': fields.Date.today(),
                        'partner_id': rec.employee_id.address_id.id or None,
                        'debit': amount < 0.0 and -amount or 0.0,
                        'credit': amount > 0.0 and amount or 0.0,
                    }
                    vals = {
                        'name': 'Over Time For' + ' ' + over_name,
                        'narration': over_name,
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
