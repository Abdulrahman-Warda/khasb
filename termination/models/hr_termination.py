# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from datetime import date, datetime


class HREmployeesTermination(models.Model):
    _name = 'hr.termination'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_set_name')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, )

    termination_type = fields.Selection(string="",
                                        selection=[('end_of_service', 'End Of Service'), ('terminate', 'Terminate'),
                                                   ('resignation', 'Resignation'), ], required=False, )

    state = fields.Selection([('draft', 'Draft'), ('manger_approved', 'Manager Approved'),
                              ('financial_manager', 'Financial Manager'), ('approved', 'Approved'),
                              ('rejected', 'Rejected'), ], string='Status', readonly=True, default='draft')

    @api.constrains('state')
    def _check_attachment(self):
        for record in self:
            if record.state == 'approved':
                if not self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', record.id)],
                                                        limit=1):
                    raise ValidationError(_('You cannot send the termination request without attaching a document.'))

    employee_company_id = fields.Many2one('res.company', readonly=True, )

    employee_department_id = fields.Many2one('hr.department', related='employee_id.department_id')

    joining_date = fields.Date(readonly=True, related='employee_id.joining_date')

    line_ids = fields.One2many('hr.termination.approvals', 'termination_id', "Approvals", readonly=True)
    notes = fields.Text()

    approved = fields.Boolean(string="", default=False)

    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    contract_joining_date = fields.Date(readonly=True, related='contract_id.date_start')
    today_date = fields.Date(readonly=True, default=fields.Date.context_today)
    duration_days = fields.Float(string="Duration/days", store=False, compute="_get_contract_months")
    duration = fields.Float(string="Duration/years", store=False, compute="_get_contract_months")
    indemnity = fields.Float(string="Total EOS", required=False, compute="_get_indemnity_value")

    refundable_advance = fields.Float(string="A refundable advance", required=False, readonly=True)
    refundable_bonus = fields.Float(string="A Refundable Bonus", required=False, readonly=True, )
    other_allowances = fields.Float(string="Other Allowances", required=False, )
    other_deductions = fields.Float(string="Other Deductions", required=False, )
    allowance_amount = fields.Float(string="", required=False, )

    saudi = fields.Boolean(string="EXCEPTION", )
    accounting_method = fields.Boolean(string="", )
    left_vacation_days = fields.Float(string="", required=False, )
    left_vacation_amount = fields.Float(string="", required=False, )
    wage_day_amount = fields.Float(string="", required=False, )
    wage = fields.Float(string="", required=False, )

    journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    account_move_id = fields.Many2one(comodel_name="account.move", string="", )
    outstanding_loans = fields.Float(string="", required=False, )

    last_working_day = fields.Date(string="", required=False, )
    last_working_days = fields.Float(string="", required=False, store=True)
    deserved_salary = fields.Float(string="", required=False, compute="_get_deserved_salary")

    comprehensive_wage = fields.Float(string="", required=False, )
    day_amount = fields.Float(string="", required=False, )
    total = fields.Float(string="", required=False, compute="_get_total")

    total_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    total_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    total_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    total_account_move_id = fields.Many2one(comodel_name="account.move", string="", )

    deserved_salary_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    deserved_salary_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_move_id = fields.Many2one(comodel_name="account.move", string="", )

    outstanding_loans_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    outstanding_loans_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_move_id = fields.Many2one(comodel_name="account.move", string="", )

    indemnity_loans_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    indemnity_loans_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    indemnity_loans_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    indemnity_loans_move_id = fields.Many2one(comodel_name="account.move", string="", )

    @api.depends('last_working_days', 'day_amount')
    def _get_deserved_salary(self):
        if self.last_working_days and self.day_amount:
            self.deserved_salary = self.last_working_days * self.day_amount
        else:
            self.deserved_salary = 0.0

    @api.depends('joining_date', 'today_date')
    def _get_contract_months(self):
        if self.today_date and self.joining_date:
            num_days = self.today_date - self.joining_date
            num_days = num_days.days
            num_years = num_days / 365
            self.duration_days = num_days
            self.duration = num_years
        else:
            self.duration_days = 0.0
            self.duration = 0.0

    def set_values(self):
        if self.employee_id:
            self.employee_company_id = self.employee_id.contract_id.company_id.id

    @api.onchange('termination_type', 'other_deductions', 'other_allowances', 'last_working_day')
    def _get_indemnity_value(self):
        if self.last_working_day:
            date_from = datetime.strptime(self.last_working_day.strftime('%Y%m%d'), '%Y%m%d')
            self.last_working_days = date_from.day
        telt = 1 / 3
        telten = 2 / 3
        if self.duration and self.today_date and self.joining_date and self.termination_type == 'end_of_service':
            if self.duration >= 2 and self.duration <= 5:
                total = self.contract_id.wage * (self.duration / 2)
                self.indemnity = total
            elif self.duration > 5:
                print("end_of_service and duration > 5")
                the_remaining_years = self.duration - 5
                total3 = (self.contract_id.wage * (5 / 2)) + (self.contract_id.wage * (the_remaining_years))
                self.indemnity = total3
            elif self.duration < 2:
                print("end_of_service and duration < 2")
                self.indemnity = 0.0
        elif self.duration and self.today_date and self.joining_date and self.termination_type == 'terminate':
            print("terminate   مش هياخد")
            self.indemnity = 0.0
        elif self.duration and self.today_date and self.joining_date and self.termination_type == 'resignation':
            if self.duration < 2 and self.saudi == False:
                print("resignation and duration < 2   مش هياخد")
                self.indemnity = 0.0
            elif self.duration >= 2 and self.duration < 5 and self.saudi == False:
                print("resignation and duration < 5   هياخد الثلث")
                total = self.contract_id.wage * (self.duration / 2)
                total3 = total * telt
                self.indemnity = total3
            elif self.duration >= 5 and self.duration < 10 and self.saudi == False:
                print("resignation and duration < 10 and not saudi    هياخد الثلثين")
                the_remaining_years = self.duration - 5
                total4 = (self.contract_id.wage * (5 / 2)) + (self.contract_id.wage * (the_remaining_years))
                total6 = total4 * telten
                self.indemnity = total6
            elif self.duration < 10 and self.saudi == True:
                print("resignation and duration < 10 and saudi    هياخد كامل")
                the_remaining_years = self.duration - 5
                total6 = (self.contract_id.wage * (5 / 2)) + (self.contract_id.wage * (the_remaining_years))
                self.indemnity = total6
            elif self.duration >= 10:
                print("resignation and duration > 10    هياخد كامل")
                the_remaining_years = self.duration - 5
                total8 = (self.contract_id.wage * (5 / 2)) + (self.contract_id.wage * (the_remaining_years))
                self.indemnity = total8
        else:
            self.indemnity = 0.0

    def current_user(self):
        return self.env.user

    def new_approval_line_dict(self):
        return {
            'user_id': self.current_user().id,
            'date_of_approval': fields.Datetime.now().date()
        }

    def create_account_move(self):
        move_line_1 = {
            'name': self.name,
            'account_id': self.debit_account_id.id,
            'debit': self.indemnity,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,
        }
        print("move_line_1 >>>>>>>>>>", move_line_1)
        move_line_2 = {
            'name': self.name,
            'account_id': self.credit_account_id.id,
            'debit': 0.0,
            'credit': self.indemnity,
        }
        print("move_line_2 >>>>>>>>>>", move_line_2)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.account_move_id = account_move.id

        move_line_3 = {
            'name': self.name or '',
            'account_id': self.total_debit_account_id.id,
            'debit': self.left_vacation_amount,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,
        }
        print("move_line_3 >>>>>>>>>>", move_line_3)

        move_line_33 = {
            'name': self.name or '',
            'account_id': self.total_credit_account_id.id,
            'debit': 0.0,
            'credit': self.left_vacation_amount,

        }
        print("move_line_33 >>>>>>>>>>", move_line_33)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.total_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_3), (0, 0, move_line_33)],
        }

        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.total_account_move_id = account_move.id

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
        }
        print("move_line_55 >>>>>>>>>>", move_line_55)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.deserved_salary_journal_id.id,
            'termination_id': self.id,
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
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_6), (0, 0, move_line_66)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.outstanding_loans_move_id = account_move.id
        move_line_7 = {
            'name': self.name or '',
            'account_id': self.indemnity_loans_credit_account_id.id,
            'debit': 0.0,
            'credit': self.indemnity,
        }
        print("move_line_7 >>>>>>>>>>", move_line_7)

        move_line_77 = {
            'name': self.name or '',
            'account_id': self.indemnity_loans_debit_account_id.id,
            'debit': self.indemnity,
            'credit': 0.0,
            'partner_id': self.employee_id.address_home_id.id or False,

        }
        print("move_line_77 >>>>>>>>>>", move_line_77)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.indemnity_loans_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_7), (0, 0, move_line_77)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.indemnity_loans_move_id = account_move.id

    @api.depends('wage_day_amount', 'duration')
    def _get_total(self):
        print("self.wage_day_amount>>", self.wage_day_amount)
        print("self.duration >>", self.duration_days)
        if self.wage_day_amount and self.duration_days:
            self.total = self.wage_day_amount * self.duration_days
        else:
            self.total = 0.0

    @api.onchange('employee_id')
    def set_employee_info(self):
        self._get_indemnity_value()
        if self.employee_id:
            loan_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ])
            if loan_obj:
                total = 0.0
                for loan in loan_obj:
                    loan_ids = loan.loan_lines.filtered(lambda x: not x.paid)
                    total += sum(loan_ids.mapped('amount'))
                self.outstanding_loans = total
            if not loan_obj:
                self.outstanding_loans = 0.0
            total = 0.0
            total_days = self.env['hr.leave.report'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            self.comprehensive_wage = self.employee_id.contract_id.wage
            self.wage_day_amount = self.employee_id.contract_id.wage / 30
            self.wage = self.employee_id.contract_id.wage
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total
            self.day_amount = self.employee_id.contract_id.wage / 30
            self.left_vacation_amount = total * self.day_amount

            self.employee_company_id = self.employee_id.company_id.id
            contracts = self.env['hr.contract'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
            if len(contracts) > 0:
                self.employee_company_id = contracts[0].company_id.id
        else:
            self.employee_company_id = False


    @api.constrains('employee_id')
    def survey_id_constrains(self):
        if self.employee_id:
            self.comprehensive_wage = self.employee_id.contract_id.wage
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
            self.comprehensive_wage = self.employee_id.contract_id.wage
            self.wage_day_amount = self.employee_id.contract_id.wage / 30
            self.wage = self.employee_id.contract_id.wage
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total
            self.day_amount = self.employee_id.contract_id.wage / 30
            self.left_vacation_amount = total * self.day_amount

            same_employee_count = self.env['hr.termination'].search_count([('employee_id', '=', self.employee_id.id)])
            if same_employee_count > 1:
                raise ValidationError(_('Employee must be unique'))
        if self.contract_id:
            self.set_values()

    @api.depends('employee_id')
    def _set_name(self):
        for rec in self:
            if rec.employee_id:
                rec.name = rec.employee_id.name + "'s Termination"
            else:
                rec.name = ''

    def change_state(self, new_state):
        self.state = new_state

    def check_if_user_approved_before(self):
        all_approval_ids = [line.user_id.id for line in self.line_ids]
        if self.current_user().id in all_approval_ids:
            return True
        return False

    def add_new_approve_line(self):
        if self.check_if_user_approved_before():
            raise ValidationError('Sorry you approved for this termination before')
        lines = [(4, line.id) for line in self.line_ids]
        lines.append((0, 0, self.new_approval_line_dict()))
        self.line_ids = lines
        group_general_supervisor = self.env.ref(
            'termination.group_can_approve_to_termination').users
        users_list = group_general_supervisor
        print('users_list >>>>>>>>>> ', users_list)
        print('users_list >>>>>>>>>> ', len(users_list))
        if len(self.line_ids) == len(users_list):
            self.state = 'financial_manager'
            self.approved = True
        if len(self.line_ids) > 0:
            self.approved == True

    def check_if_current_user_has_group(self, group_id):
        return self.current_user().has_group(group_id)

    def manager_approve_validation(self):
        if self.employee_id.parent_id and self.employee_id.parent_id.user_id:
            return self.current_user().id == self.employee_id.parent_id.user_id.id
        else:
            return self.check_if_current_user_has_group('hr.group_hr_manager')

    def manager_approve(self):
        print("manager_approve")
        if not (self.manager_approve_validation()):
            raise ValidationError("Sorry you are not the employee's manager")
        else:
            self.add_new_approve_line()
            self.change_state('manger_approved')

    def approvals(self):
        print("approvals")
        if not (self.check_if_current_user_has_group('termination.group_can_approve_to_termination')):
            raise ValidationError('Sorry you cannot approve a termination')
        self.add_new_approve_line()

    def financial_manager_approve(self):
        self.state = 'approved'
        self.create_account_move()

    def reject(self):
        print("reject")
        if self.check_if_user_approved_before():
            raise ValidationError('You have approved to this termination so you cannot reject it')
        if self.state == 'draft' and not (self.manager_approve_validation()):
            raise ValidationError("Sorry you cannot reject this termination because you are not the employee's manager")
        if self.state == 'manger_approved' and not (
                self.check_if_current_user_has_group('termination.group_can_approve_to_termination')):
            raise ValidationError("Sorry you cannot reject this termination")
        self.change_state('rejected')


class HREmployeesEvaluationQuestions(models.Model):
    _name = 'hr.termination.approvals'
    termination_id = fields.Many2one('hr.termination')
    user_id = fields.Many2one('res.users', required=True)
    date_of_approval = fields.Date()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    joining_date = fields.Date(readonly=False, )
