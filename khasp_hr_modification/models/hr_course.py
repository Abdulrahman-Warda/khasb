# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
class khasp_hr_course_modification(models.Model):
    _inherit = 'hr.course'
    state = fields.Selection(
        [('draft', 'Department Manger'),
         ('general_manger', 'General Manger'),
         ('hr_manger', 'HR Manger'),
         ('completed', 'Confirm'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )

    debit_account_id = fields.Many2one(comodel_name="account.account", string="Debit Account", required=False)
    credit_account_id = fields.Many2one(comodel_name="account.account", string="Credit Account", required=False)
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=False)
    move_id = fields.Many2one(comodel_name="account.move", string="Move", required=False)

    def create_move(self):
        if self.move_id:
            raise ValidationError("Move Entry Created")
        debit_line={
            'name': self.name,
            'account_id': self.debit_account_id.id,
            'credit':0 ,
            'debit': self.cost,
        }
        credit_line = {
            'name': self.name,
            'account_id': self.debit_account_id.id,
            'credit': self.cost,
            'debit':0 ,
        }

        self.move_id=self.env['account.move'].create({
            'journal_id':self.journal_id.id,
            'name':self.name+str(datetime.now().date()),
            'date':datetime.now().date(),
            'journal_id':self.journal_id.id,
            'line_ids':[(0,0,debit_line),(0,0,credit_line)],
        })




    def action_department_manger(self):
        for rec in self:
            mangers=[]

            current_user = self.env.uid
            departments=self.env['hr.department'].search([])

            for department in departments:
                mangers.append(department.manager_id.user_id.id)

            if current_user not in mangers:
                raise ValidationError("you can\'t approve this request")
            rec.state = 'general_manger'
    def action_general_manger(self):
        for rec in self:
            rec.state = 'hr_manger'
    def action_hr_manger(self):
        for rec in self:
            rec.state = 'confirm'
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    def set_draft(self):
        for rec in self:
            rec.state = 'draft'



