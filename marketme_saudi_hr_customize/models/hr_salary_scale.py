""" Initialize Hr Salary Scale """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrSalaryScale(models.Model):
    """
        Initialize Hr Salary Scale:
         -
    """
    _name = 'hr.salary.scale'
    _description = 'Hr Salary Scale'

    # def default_basic_salary(self):
    #     return self.basic_salary

    name = fields.Char(
        required=True,
        translate=True,
    )
    basic_salary = fields.Monetary(
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
    )
    housing_compute_type = fields.Selection(
        [('amount', 'amount'),
         ('percent', 'percent')],
        default='amount',
    )
    transfer_compute_type = fields.Selection(
        [('amount', 'amount'),
         ('percent', 'percent')],
        default='amount',
    )
    transfer_allowances_amount = fields.Float()
    transfer_allowances = fields.Float(
        compute='_compute_transfer_allowances'
    )
    internal_mandate_compute_type = fields.Selection(
        [('amount', 'amount'),
         ('percent', 'percent')],
        default='amount',
    )
    internal_mandate_allowances_amount = fields.Float()
    internal_mandate_allowances = fields.Float(
        compute='_compute_internal_mandate_allowances'
    )
    external_mandate_compute_type = fields.Selection(
        [('amount', 'amount'),
         ('percent', 'percent')],
        default='amount',
    )
    external_mandate_allowances_amount = fields.Float()
    external_mandate_allowances = fields.Float(
        compute='_compute_external_mandate_allowances'
    )
    housing_allowances_amount = fields.Float()
    housing_allowances = fields.Float(
        compute='_compute_housing_allowances'
    )
    # employee_percent = fields.Float()
    # company_percent = fields.Float()
    # insurance_salary = fields.Float(
    #     default=default_basic_salary,
    # )

    food_allowances = fields.Float()
    phone_allowances = fields.Float()
    other_allowances = fields.Float()
    bank_expenses = fields.Float()
    other_deductions = fields.Float()

    @api.depends('basic_salary', 'external_mandate_compute_type', 'external_mandate_allowances_amount')
    def _compute_external_mandate_allowances(self):
        """ Compute  value """
        for rec in self:
            if rec.external_mandate_compute_type == 'percent':
                rec.external_mandate_allowances = rec.basic_salary * (rec.external_mandate_allowances_amount / 100)
            else:
                rec.external_mandate_allowances = rec.external_mandate_allowances_amount

    @api.depends('basic_salary', 'internal_mandate_compute_type', 'internal_mandate_allowances_amount')
    def _compute_internal_mandate_allowances(self):
        """ Compute  value """
        for rec in self:
            if rec.internal_mandate_compute_type == 'percent':
                rec.internal_mandate_allowances = rec.basic_salary * (rec.internal_mandate_allowances_amount / 100)
            else:
                rec.internal_mandate_allowances = rec.internal_mandate_allowances_amount

    @api.depends('basic_salary', 'transfer_compute_type')
    def _compute_transfer_allowances(self):
        """ Compute  value """
        for rec in self:
            if rec.transfer_compute_type == 'percent':
                rec.transfer_allowances = rec.basic_salary * (rec.transfer_allowances_amount / 100)
            else:
                rec.transfer_allowances = rec.transfer_allowances_amount

    @api.depends('basic_salary', 'housing_compute_type')
    def _compute_housing_allowances(self):
        """ Compute  value """
        for rec in self:
            if rec.housing_compute_type == 'percent':
                rec.housing_allowances = rec.basic_salary * (rec.housing_allowances_amount / 100)
            else:
                rec.housing_allowances = rec.housing_allowances_amount

    @api.constrains('transfer_compute_type', 'transfer_allowances_amount')
    def _check_transfer_allowances_amount(self):
        """ Validate  """
        for rec in self:
            if rec.transfer_compute_type == 'percent' and rec.transfer_allowances_amount > 100:
                raise ValidationError('Percent must be lower than 100 %')

    @api.constrains('housing_compute_type', 'housing_allowances_amount')
    def _check_housing_allowances_amount(self):
        """ Validate  """
        for rec in self:
            if rec.housing_compute_type == 'percent' and rec.housing_allowances_amount > 100:
                raise ValidationError('Percent must be lower than 100 %')
