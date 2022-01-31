# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import Warning, ValidationError


class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", default="New", readonly=True, copy=False)

    state = fields.Selection(string="", selection=[('hr_manager', 'Hr Manager'),
                                                   ('direct_manager', 'Direct Manager'),
                                                   ('financial_manager', 'Financial Manager'),
                                                   ('confirm', 'Confirm'),
                                                   ('rejected', 'Rejected'), ], required=False,
                             default='hr_manager')

    @api.constrains('state')
    def _check_attachment(self):
        for record in self:
            if record.state == 'confirm':
                if not self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', record.id)],
                                                        limit=1):
                    raise ValidationError(_('You cannot send the vacation request without attaching a document.'))

    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('business.trip')) or 'New'
        return super(BusinessTrip, self).create(vals)

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee Name", required=False, )
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    country_id = fields.Many2one(comodel_name="res.country.state", string="Country Name", required=False, )
    today_date = fields.Date(string="From Date", required=False, readonly=False, default=fields.Date.context_today)
    return_date = fields.Date(string="Return Date", required=False, )
    reason = fields.Text(string="Reason", required=False, )
    left_vacation_days = fields.Float(string="", required=False, )
    duration = fields.Float(string="Duration / Days", store=False, compute="_get_duration")
    Total_price = fields.Float(string="Total Price", required=False, compute='get_total_price')
    last_working_day = fields.Date(string="", required=False, )
    last_working_days = fields.Float(string="", required=False, store=True)
    day_amount = fields.Float(string="", required=False, )
    wage = fields.Float(string="", required=False, )
    total = fields.Float(string="", required=False, compute="_get_total")
    deserved_salary = fields.Float(string="", required=False, compute="_get_deserved_salary")
    ticket_allowance = fields.Float(string="", required=False, store=True)
    add_house_allowance = fields.Boolean(string="", default=False)
    add_ticket_allowance = fields.Boolean(string="", default=False)
    add_outstanding_loans = fields.Boolean(string="", default=False)
    outstanding_loans = fields.Float(string="", required=False, )

    total_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    total_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    total_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    total_account_move_id = fields.Many2one(comodel_name="account.move", string="", )

    ticket_allowance_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    ticket_allowance_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    ticket_allowance_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    ticket_allowance_move_id = fields.Many2one(comodel_name="account.move", string="", )

    deserved_salary_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    deserved_salary_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_move_id = fields.Many2one(comodel_name="account.move", string="", )

    outstanding_loans_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    outstanding_loans_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_move_id = fields.Many2one(comodel_name="account.move", string="", )

    @api.depends('return_date', 'today_date')
    def _get_duration(self):
        if self.return_date and self.today_date:
            num_days = self.return_date - self.today_date
            num_days = num_days.days
            self.duration = num_days
        else:
            self.duration = 0.0

    @api.depends('day_amount', 'duration')
    def _get_total(self):
        if self.day_amount and self.duration:
            self.total = self.day_amount * self.duration
        else:
            self.total = 0.0

    @api.depends('last_working_days', 'day_amount')
    def _get_deserved_salary(self):
        if self.last_working_days and self.day_amount:
            self.deserved_salary = self.last_working_days * self.day_amount
        else:
            self.deserved_salary = 0.0

    @api.onchange('employee_id', 'left_vacation_days', 'today_date', 'return_date', 'last_working_day')
    def set_employee_info(self):
        if self.employee_id:
            print("####################",self.employee_id.contract_id.wage)
            print("####################",self.employee_id.contract_id.wage)
            loan_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ])
            if loan_obj:
                total = 0.0
                for loan in loan_obj:
                    loan_ids = loan.loan_lines.filtered(lambda x: not x.paid)
                    total += sum(loan_ids.mapped('amount'))
                self.outstanding_loans = total
            if not loan_obj:
                self.outstanding_loans = 0.0
            self.day_amount = self.employee_id.contract_id.wage / 30
            self.wage = self.employee_id.contract_id.wage
            total = 0.0
            total_days = self.env['hr.leave.report'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total

        if self.employee_id and self.left_vacation_days and self.today_date and self.return_date:
            if self.duration <= self.left_vacation_days:
                self.Total_price = self.employee_id.contract_id.wage / 30 * self.duration
            elif self.duration > self.left_vacation_days:
                print("ahmed")
                self.sudo().write({
                    'Total_price': self.left_vacation_days
                })
                raise ValidationError('Sorry you Cant take days more than %s' % self.left_vacation_days)

        if self.last_working_day:
            date_from = datetime.strptime(self.last_working_day.strftime('%Y%m%d'), '%Y%m%d')
            self.last_working_days = date_from.day

        else:
            self.last_working_days = False
            self.Total_price = 0.0

    def create_account_move(self):
        move_line_3 = {
            'name': self.name or '',
            'account_id': self.total_debit_account_id.id,
            'debit': self.total,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,
        }
        print("move_line_3 >>>>>>>>>>", move_line_3)

        move_line_33 = {
            'name': self.name or '',
            'account_id': self.total_credit_account_id.id,
            'debit': 0.0,
            'credit': self.total,
        }
        print("move_line_33 >>>>>>>>>>", move_line_33)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.total_journal_id.id,
            'trip_id': self.id,
            'line_ids': [(0, 0, move_line_3), (0, 0, move_line_33)],
        }

        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.total_account_move_id = account_move.id

        move_line_4 = {
            'name': self.name or '',
            'account_id': self.ticket_allowance_debit_account_id.id,
            'debit': self.ticket_allowance,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,

        }
        print("move_line_4 >>>>>>>>>>", move_line_4)

        move_line_44 = {
            'name': self.name or '',
            'account_id': self.ticket_allowance_credit_account_id.id,
            'debit': 0.0,
            'credit': self.ticket_allowance,
        }
        print("move_line_44 >>>>>>>>>>", move_line_44)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.ticket_allowance_journal_id.id,
            'trip_id': self.id,
            'line_ids': [(0, 0, move_line_4), (0, 0, move_line_44)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.ticket_allowance_move_id = account_move.id

        move_line_5 = {
            'name': self.name or '',
            'account_id': self.deserved_salary_debit_account_id.id,
            'debit': self.deserved_salary,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,

        }
        print("move_line_5 >>>>>>>>>>", move_line_5)

        move_line_55 = {
            'name': self.name or '',
            'account_id': self.deserved_salary_credit_account_id.id,
            'debit': 0.0,
            'credit': self.deserved_salary,
            'partner_id': self.employee_id.address_home_id.id or False,

        }
        print("move_line_55 >>>>>>>>>>", move_line_55)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.deserved_salary_journal_id.id,
            'trip_id': self.id,
            'line_ids': [(0, 0, move_line_5), (0, 0, move_line_55)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.deserved_salary_move_id = account_move.id

        move_line_6 = {
            'name': self.name or '',
            'account_id': self.outstanding_loans_credit_account_id.id,
            'debit': 0.0,
            'credit': self.outstanding_loans,
            'partner_id': self.employee_id.address_home_id.id or False,

        }
        print("move_line_6 >>>>>>>>>>", move_line_6)

        move_line_66 = {
            'name': self.name or '',
            'account_id': self.outstanding_loans_debit_account_id.id,
            'debit': self.outstanding_loans,
            'credit': 0.0,
        }
        print("move_line_66 >>>>>>>>>>", move_line_66)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.outstanding_loans_journal_id.id,
            'trip_id': self.id,
            'line_ids': [(0, 0, move_line_6), (0, 0, move_line_66)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.outstanding_loans_move_id = account_move.id

    @api.constrains('employee_id')
    def survey_id_constrains(self):
        if self.employee_id:
            self.day_amount = self.employee_id.contract_id.wage / 30
            if self.last_working_day:
                date_from = datetime.strptime(self.last_working_day.strftime('%Y%m%d'), '%Y%m%d')
                self.last_working_days = date_from.day
            elif not self.last_working_day:
                self.last_working_days = False
            loan_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ])
            if loan_obj:
                total = 0.0
                for loan in loan_obj:
                    loan_ids = loan.loan_lines.filtered(lambda x: not x.paid)
                    print(loan_obj)
                    total += sum(loan_ids.mapped('amount'))
                self.outstanding_loans = total
            if not loan_obj:
                self.outstanding_loans = 0.0

            total = 0.0
            total_days = self.env['hr.leave.report'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total
            if self.duration <= self.left_vacation_days:
                self.Total_price = self.employee_id.contract_id.wage / 30 * self.duration
            elif self.duration > self.left_vacation_days:
                print("ahmed")
                self.sudo().write({
                    'Total_price': self.left_vacation_days
                })
                raise ValidationError('Sorry you Cant take days more than %s' % self.left_vacation_days)

    @api.depends('employee_id', 'duration', 'deserved_salary', 'ticket_allowance', 'deserved_salary',
                 'outstanding_loans', 'add_ticket_allowance', 'add_outstanding_loans', 'add_house_allowance')
    def get_total_price(self):
        saber_total = 0.0
        if self.employee_id:
            if self.duration <= self.left_vacation_days:
                self.Total_price += self.employee_id.contract_id.wage / 30 * self.duration
            if self.add_house_allowance == True:
                self.Total_price += self.employee_id.contract_id.house_allow
            if self.add_ticket_allowance == True:
                self.Total_price += self.ticket_allowance
            if self.add_outstanding_loans == True:
                self.Total_price -= self.outstanding_loans
            if self.deserved_salary > 0:
                self.Total_price += self.deserved_salary
            else:
                return
        else:
            self.Total_price = 0.0

        print(" >>>>>>>>>>>>>>>>>>>>>>>> ", saber_total)

    def hr_manager(self):
        for rec in self:
            rec.state = 'direct_manager'

    def direct_manager(self):
        for rec in self:
            if rec.env.user.id == rec.employee_id.parent_id.user_id.id or rec.env.user.has_group(
                    "hr.group_hr_manager") or rec.env.user.has_group("hr.group_hr_user"):
                rec.state = 'financial_manager'
            else:
                raise ValidationError("Only Employee Manger Can Approve That!")

    def financial_manager(self):
        for rec in self:
            self.create_account_move()
            date_from = datetime.strptime(rec.today_date.strftime('%Y%m%d'), '%Y%m%d')
            date_to = datetime.strptime(rec.return_date.strftime('%Y%m%d'), '%Y%m%d')
            vals = {
                'holiday_status_id': self.env['hr.leave.type'].search([('leave_type', '=', 'paid')],
                                                                      limit=1).id,
                'name': 'business trip Holiday For Employee %s' % rec.employee_id.name,
                'holiday_type': 'employee',
                'employee_id': rec.employee_id.id,
                'request_date_from': rec.today_date,
                'date_from': date_from,
                'request_date_to': rec.return_date,
                'date_to': date_to,
                'number_of_days': rec.duration,
                'number_of_days_display': rec.duration,
            }
            print("vals", vals)
            hol = self.env['hr.leave'].create(vals)
            print("Ahmed Saber", hol)
            rec.state = 'confirm'
            self.employee_id.active = False

    def reject(self):
        for rec in self:
            rec
            rec.state = 'rejected'

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    trip_id = fields.Many2one(comodel_name="business.trip", string="", required=False, )