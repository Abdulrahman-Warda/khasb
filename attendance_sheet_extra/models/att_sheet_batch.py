# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2018-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################


import pytz
from datetime import datetime,date, timedelta,time
from dateutil.relativedelta import relativedelta
from odoo import models, fields, tools, api, exceptions, _
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import  UserError,ValidationError
import babel
from operator import itemgetter
import logging
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"


class attendance_sheet_batch(models.Model):
    _name = 'attendance.sheet.batch'
    name = fields.Char("name")
    department_id = fields.Many2one('hr.department', 'Department Name', required=True)
    date_from = fields.Date(string='Date From', readonly=True, required=True,
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)), )
    date_to = fields.Date(string='Date To', readonly=True, required=True,
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    att_sheet_ids = fields.One2many(comodel_name='attendance.sheet', string='Attendance Sheets',
                                    inverse_name='batch_id')
    payslip_batch_id=fields.Many2one(comodel_name='hr.payslip.run',string='Payslip Batch')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('att_gen', 'Attendance Sheets Generated'),
        ('att_sub', 'Attendance Sheets Submitted'),
        ('done', 'Close')], default='draft', track_visibility='onchange',
        string='Status', required=True, readonly=True, index=True, )

    # employee_ids = fields.Many2many('hr.employee', 'hr_att_wizard_rel', 'att_wizard_id', 'employee_id', 'Employees')



    @api.onchange('department_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.department_id) or (not self.date_from) or (not self.date_to):
            return
        department = self.department_id
        date_from = self.date_from
        date_to = self.date_to

        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        locale = self.env.context.get('lang', 'en_US')
        self.name = _('Attendance Batch of %s  Department for %s') % (department.name,
                                                                      tools.ustr(
                                                                          babel.dates.format_date(date=ttyme,
                                                                                                  format='MMMM-y',
                                                                                                  locale=locale)))


    @api.multi
    def action_done(self):
        for batch in self:
            if batch.state != "att_sub":
                continue
            for sheet in batch.att_sheet_ids:
                if sheet.state == 'confirm':
                    sheet.action_attsheet_approve()
                    sheet.create_payslip_id()
            batch.write({'state': 'done'})



    @api.multi
    def action_att_gen(self):
        return self.write({'state': 'att_gen'})

    @api.multi
    def gen_att_sheet(self):

        att_sheets = self.env['attendance.sheet']
        for batch in self:
            from_date = batch.date_from
            to_date = batch.date_to
            employee_ids = self.env['hr.employee'].search([('department_id', '=', batch.department_id.id)])
            print('iam in generate sheets and employees is',employee_ids)
            if not employee_ids:
                raise UserError(_("There is no  Employees In This Department"))
            for employee in employee_ids:
                print ('employee is ',employee.name)
                contract_ids = self.env['hr.payslip'].get_contract(employee, from_date, to_date)
                print ('contracts od employee is',contract_ids)
                if not contract_ids:
                    raise UserError(_("There is no  Running contracts for :%s "%employee.name))
                contract = self.env['hr.contract'].browse(contract_ids[0])
                att_data = self.env['attendance.sheet'].onchange_employee_id(from_date, to_date, employee.id)
                print('att data is',att_data)
                res = {
                    'employee_id': employee.id,
                    'name': att_data['value'].get('name'),
                    'month':att_data['value'].get('month'),
                    'year': att_data['value'].get('year'),
                    'batch_id': batch.id,
                    'date_from': from_date,
                    'date_to': to_date,
                    'att_policy_id': att_data['value'].get('att_policy_id')
                    }
                print(res)
                att_sheet = self.env['attendance.sheet'].create(res)
                att_sheet.get_attendances()
                att_sheets += att_sheet
            batch.action_att_gen()

    @api.multi
    def submit_att_sheet(self):
        for batch in self:
            if batch.state !="att_gen":
                continue
            for sheet in batch.att_sheet_ids:
                if sheet.state=='draft':
                    sheet.action_attsheet_confirm()

            batch.write({'state': 'att_sub'})










