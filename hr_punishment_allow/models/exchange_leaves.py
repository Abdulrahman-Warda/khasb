# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class Exchange(models.Model):
    _name='hr.exchange.leaves'
    _rec_name='employee_id'
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True,states={'confirm': [('readonly', True)]})
    type = fields.Selection(string="Type", selection=[('add', 'Add'), ('decrease', 'Decrease'), ], required=True,states={'confirm': [('readonly', True)]})
    allocation = fields.Many2one(comodel_name="hr.leave.allocation", string="Allocation", required=True,states={'confirm': [('readonly', True)]})
    state = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ],required=False, default='draft',states={'confirm': [('readonly', True)]})
    days = fields.Integer(string="Days", required=False,states={'confirm': [('readonly', True)]})
    amount = fields.Float(string="Amount", required=False,states={'confirm': [('readonly', True)]})
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=True,states={'confirm': [('readonly', True)]})
    payment_id = fields.Many2one(comodel_name="account.payment", string="Payment", required=False,states={'confirm': [('readonly', True)]})

    def confirm(self):
        res=self.create_payment()
        print(">S", res)
        self.payment_id = res.id
        self.state='confirm'



    def create_payment(self):
        if self.type=='decrease':
            res=self.env['account.payment'].create({
                'partner_type': 'supplier',
                'payment_type': 'outbound',
                'partner_id': self.employee_id.user_id.partner_id.id,
                'journal_id': self.journal_id.id,
                'company_id': self.env.user.company_id.id,
                'payment_method_id': self.env['account.payment.method'].search([],limit=1).id,
                'amount': self.amount,
                'currency_id': self.env.user.company_id.currency_id.id,
                'payment_date':datetime.now().date(),
                'writeoff_label': 'exchange Leaves'
            })

            self.allocation.write({'number_of_days':self.allocation.number_of_days-self.days})
            return res
        else:
            res=self.env['account.payment'].create({
                'partner_type': 'customer',
                'payment_type': 'inbound',
                'partner_id': self.employee_id.user_id.partner_id.id,
                'journal_id': self.journal_id.id,
                'company_id': self.env.user.company_id.id,
                'payment_method_id': self.env['account.payment.method'].search([], limit=1).id,
                'amount': self.amount,
                'currency_id': self.env.user.company_id.currency_id.id,
                'payment_date': datetime.now().date(),
                'writeoff_label': 'exchange Leaves'})
            self.allocation.write({'number_of_days':self.allocation.number_of_days+self.days})
            return res


