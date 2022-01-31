# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit='hr.contract'

    house_allow = fields.Float(string="House Allowance", required=False,store=True,readonly=False)
    trans_allow = fields.Float(string="Transporation Allowance", required=False,store=True,readonly=False)
    phone_allow = fields.Float(string="Phone Allowance", required=False,readonly=False)
    food_allow = fields.Float(string="Food Allowance", required=False,readonly=False)
    other_allow = fields.Float(string="Other Allowance", required=False,readonly=False)

    is_saudi = fields.Boolean(string="Is Saudi?")

    ded_gosi = fields.Float(string="Gosi", required=False)
    ded_employee_gosi = fields.Float(string="Employee Gosi", required=False)
    ded_company_gosi = fields.Float(string="Company Gosi", required=False)
    ded_bank_fees = fields.Float(string="Bank Fees", required=False)
    ded_other = fields.Float(string="Other Deduction", required=False)

    annual_days = fields.Integer(string="عدد أيام الإجازة السنوية", required=False)

    @api.onchange('state')
    def onchange_to_calc_annual_days(self):
        if self.state=='open':
            self.create_alloc(self.employee_id,self.annual_days)

    def create_alloc(self, employee_id, days):
        vals = {
            'holiday_status_id': self.env['hr.leave.type'].search([('annual','=',True)],limit=1).id,
            'holiday_type': 'employee',
            'employee_id': employee_id.id,
            'name': employee_id.name,
            'number_of_days': days,
        }
        self.env['hr.leave.allocation'].create(vals)
        return True

    @api.one
    @api.depends('wage','is_saudi')
    def calc_allow_ded(self):
      self.house_allow=self.wage*.25
      self.trans_allow=self.wage*.10
      if self.is_saudi:
          self.ded_gosi=(self.wage+self.house_allow)*0.22
          self.ded_employee_gosi=(self.wage+self.house_allow)*0.1
          self.ded_company_gosi=(self.wage+self.house_allow)*0.12
