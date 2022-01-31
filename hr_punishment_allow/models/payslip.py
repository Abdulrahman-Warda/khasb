# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Payslip(models.Model):
    _inherit='hr.payslip'

    punishment_amount = fields.Float(string="Punishment Amount",compute='_clalc_punishment_amount',store=True)

    @api.one
    @api.depends('date_from','date_to','employee_id')
    def _clalc_punishment_amount(self):
        domain1=[]
        domain2=[]
        if self.employee_id:
            domain1.append(('employee_id', '=', self.employee_id.id))

        if self.employee_id:
            domain2.append(('department_id', '=', self.employee_id.department_id.id))

        if self.date_from:
            domain1.append(('date', '>=', str(self.date_from)))
            domain2.append(('date', '>=', str(self.date_from)))
        if self.date_to:
            domain1.append(('date', '<=', str(self.date_to)))
            domain2.append(('date', '<=', str(self.date_to)))
        list = self.env['hr.punishment'].search(domain1,limit=1) or self.env['hr.punishment'].search(domain2,limit=1)
        if list:
            self.punishment_amount=list.amount


