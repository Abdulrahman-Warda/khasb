""" Initialize Hr Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrContract(models.Model):
    """
        Inherit Hr Contract:
         -
    """
    _inherit = 'hr.contract'

    @api.onchange('salary_scale_id')
    def update_contract_components(self):
        self.wage = self.salary_scale_id.basic_salary
        self.house_allow = self.salary_scale_id.housing_allowances
        self.trans_allow = self.salary_scale_id.transfer_allowances
        self.internal_mandate_allowances = self.salary_scale_id.internal_mandate_allowances
        self.external_mandate_allowances = self.salary_scale_id.external_mandate_allowances
        self.food_allow = self.salary_scale_id.food_allowances
        self.phone_allow = self.salary_scale_id.phone_allowances
        self.other_allow = self.salary_scale_id.other_allowances
        self.ded_bank_fees = self.salary_scale_id.bank_expenses
        self.ded_other = self.salary_scale_id.other_deductions

    # internal_travel_allowances = fields.Float()
    # abroad_travel_allowances = fields.Float()
    # other_travel_allowances = fields.Float()
    # hour_travel_allowances = fields.Float()
    hiring_date = fields.Date()
    work_days_per_month = fields.Float()
    work_hours_per_day = fields.Float()
    hour_rate = fields.Float(
        compute='_compute_hour_rate'
    )
    salary_scale_id = fields.Many2one(
        'hr.salary.scale'
    )
    # transfer_allowances = fields.Float(
    #     related='salary_scale_id.transfer_allowances',
    #     store=1,
    #     readonly=0
    # )
    # housing_allowances = fields.Float(
    #     related='salary_scale_id.housing_allowances',
    #     store=1,
    #     readonly=0
    # )
    # wage = fields.Monetary(
    #     related='salary_scale_id.basic_salary',
    #     store=1,
    #     readonly=0
    # )
    # food_allowances = fields.Float(
    #     related='salary_scale_id.food_allowances',
    #     store=1,
    #     readonly=0
    # )
    # phone_allowances = fields.Float(
    #     related='salary_scale_id.phone_allowances',
    #     store=1,
    #     readonly=0
    # )
    # other_allowances = fields.Float(
    #     related='salary_scale_id.other_allowances',
    #     store=1,
    #     readonly=0
    # )
    bank_expenses = fields.Float(
        related='salary_scale_id.bank_expenses',
        store=1,
        readonly=0
    )
    other_deductions = fields.Float(
        related='salary_scale_id.other_deductions',
        store=1,
        readonly=0
    )
    internal_mandate_allowances = fields.Float(
        related='salary_scale_id.internal_mandate_allowances',
        store=1,
        readonly=0
    )
    external_mandate_allowances = fields.Float(
        related='salary_scale_id.external_mandate_allowances',
        store=1,
        readonly=0
    )
    # employee_percent = fields.Float(
    #     related='salary_scale_id.employee_percent',
    #     store=1,
    #     readonly=0
    # )
    # company_percent = fields.Float(
    #     related='salary_scale_id.company_percent',
    #     store=1,
    #     readonly=0
    # )
    # insurance_salary = fields.Float(
    #     compute='get_insurance_salary'
    # )
    # company_amount = fields.Float(string="",  compute='get_insurance_salary' )
    # employee_amount = fields.Float(string="",  compute='get_insurance_salary' )
    #
    # @api.depends('wage','housing_allowances','company_percent','employee_percent')
    # def get_insurance_salary(self):
    #     for rec in self:
    #         insurance_salary = rec.wage + rec.housing_allowances
    #         company_amount = (rec.company_percent / 100) * insurance_salary
    #         employee_amount = (rec.employee_percent / 100) * insurance_salary
    #         rec.insurance_salary = insurance_salary
    #         rec.company_amount = company_amount
    #         rec.employee_amount = employee_amount

    @api.depends('work_days_per_month', 'work_hours_per_day', 'wage')
    def _compute_hour_rate(self):
        """ Compute hour_rate value """
        for rec in self:
            if rec.work_days_per_month > 0 and rec.work_hours_per_day > 0:
                rec.hour_rate = (rec.wage / rec.work_days_per_month / rec.work_hours_per_day)
            else:
                rec.hour_rate = 0
