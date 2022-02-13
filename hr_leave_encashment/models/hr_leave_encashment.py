from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, time
from odoo.tools import date_utils
from odoo.tools.float_utils import float_round

class HrLeaveEncashment(models.Model):
    _name = 'hr.leave.encashment'
    _description = 'Leaves Encashment'
    _inherit = 'mail.thread'

    name = fields.Many2one('hr.employee')
    holiday_ids = fields.Many2many('hr.leave')
    calculation_mode = fields.Selection([('wage','Basic Salary'),('new_wage','Total Salary')])
    available_days = fields.Float(compute="_compute_available_days")
    request_days = fields.Float()
    day_amount = fields.Float(compute="_compute_day_amount")
    total_encashment = fields.Float(compute="_compute_total_encashment")
    payment_type = fields.Selection([('move_id','In Journal Entry'),('payslip_id','In Payslip')], default="payslip_id")
    move_id = fields.Many2one('account.move')
    journal_id = fields.Many2one('account.journal')
    credit_account_id = fields.Many2one('account.account')
    debit_account_id = fields.Many2one('account.account')
    # is_processed = fields.Boolean(track_visibility='always', default=False)
    process_date = fields.Date()

    state = fields.Selection([('draft','Draft'),('submit','Submitted'),('process','Processed')], default="draft", track_visibility='always')

    @api.onchange('name','holiday_ids')
    def _compute_available_days(self):
        for this in self:
            if this.name and this.holiday_ids:
                this.available_days = sum(this.holiday_ids.mapped('number_of_days_display'))
            else:
                this.available_days = 0.0

    # @api.onchange('calculation_mode','name')
    def _compute_day_amount(self):
        for this in self:
            if this.name and this.calculation_mode:
                if this.calculation_mode == 'wage':
                    this.day_amount = self.name.contract_id.wage / 26
                elif this.calculation_mode == 'new_wage':
                    this.day_amount = self.name.contract_id.new_wage / 26
            else:
                this.day_amount = 0.0


    @api.onchange('request_days')
    def _compute_total_encashment(self):
        for this in self:
            this.total_encashment = this.request_days * this.day_amount


    @api.onchange('request_days')
    def _request_days_constrains(self):
        if self.name and self.holiday_ids:
            if self.request_days > self.available_days or self.request_days <= 0:
                raise ValidationError("You can not request this amount of days")


    def action_submit(self):
        self.state = 'submit'
    def action_process(self):
        if self.request_days > self.available_days or self.request_days <= 0:
            raise ValidationError("You can not request this amount of days")
        if self.payment_type == 'payslip_id':
            self.state = 'process'
        else:
            if not self.credit_account_id or not self.debit_account_id or not self.journal_id:
                raise UserError("You must enter accounting information to process ")
            amount = self.total_encashment
            name = self.name.id
            reference = self.name.name
            journal_id = self.journal_id.id
            debit_account_id = self.debit_account_id.id
            credit_account_id = self.credit_account_id.id
            debit_vals = {
                'name': name,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'date': self.process_date,
                'partner_id': self.name.address_id.id or None,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
            }
            credit_vals = {
                'name': name,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': self.process_date,
                'partner_id': self.name.address_id.id or None,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
            }
            vals = {
                'narration': name,
                'ref': reference,
                'partner_id': self.name.address_id.id or None,
                'journal_id': journal_id,
                'date': self.process_date,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.post()
            self.move_id = move.id
            self.state = 'process'
        for leave in self.holiday_ids:
            leave.is_encashmented = True
        # if self.state == 'process':
        #     last_leave = self.env['hr.leave'].search([('holiday_status_id','=',self.holiday_status_id.id),('employee_id','=',self.name.id),('state','=','validate')])
        #     if len(last_leave) > 0:
        #         new_leave_request = self.env['hr.leave'].create({
        #         'name':'Encashment',
        #         'employee_id':self.name.id,
        #         'request_date_from':last_leave[-1].request_date_to + timedelta(days=1),
        #         'request_date_to':last_leave[-1].request_date_to + timedelta(days=1+self.request_days),
        #         'is_encashment_leave':True,
        #         'holiday_type':'employee',
        #         'department_id':self.name.department_id.id,
        #         'state':'validate',
        #         'holiday_status_id':self.holiday_status_id.id
        #         })
        #     else:
        #         new_leave_request = self.env['hr.leave'].create({
        #         'name':'Encashment',
        #         'employee_id':self.name.id,
        #         'request_date_from':date_utils.start_of(fields.Date.today(), "year"),
        #         'request_date_to':date_utils.start_of(fields.Date.today(), "year") + timedelta(days=self.request_days),
        #         'number_of_days_display':self.request_days,
        #         'number_of_days':self.request_days,
        #         'is_encashment_leave':True,
        #         'holiday_type':'employee',
        #         'department_id':self.name.department_id.id,
        #         'state':'validate',
        #         'holiday_status_id':self.holiday_status_id.id
        #         })
