# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime
from datetime import date, timedelta, datetime
import time
from dateutil import tz
from dateutil.relativedelta import relativedelta


class EmployeeInsuranceReportWizard(models.TransientModel):
    _name = "employee.insurance.report"
    _description = "Employee Insurance Report wizard"

    report_for = [("1", "All Employees"),
                  ("2", "Select Employee"), ]

    report_for = fields.Selection(report_for, string="Report For", default='1')

    employee_ids = fields.Many2many('hr.employee', string="Employees")

    # TODO Print report
    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read(['employee_ids', ])[0]
        return self.env.ref('hr_employee_contract.action_employee_insurance_pdf').with_context(landscape=True).report_action(self, data=data,
                                                                                                config=False)

    # # TODO preview report
    # @api.multi
    # def preview_report(self):
    #     print("ahmed saber")
        # data = {}
        # data['form'] = self.read(['course_training_id', 'employee_ids', 'date_from', 'date_to'])[0]
        # return self.env.ref('cs_reports.action_employee_course_schedule_report_html').report_action(self, data=data,config=False)


class EmployeeInsuranceReport(models.AbstractModel):
    _name = 'report.hr_employee_contract.employee_insurance_reportt'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        check_report = self.env['ir.actions.report']._get_report_from_name(
            'hr_employee_contract.action_employee_insurance_pdf')
        employee_ids = docs.employee_ids
        report_for = docs.report_for

        all_employee_insurance = []

        print("Ahmed Saber")
        if report_for == '1':
            print("11111111111111111111111111")
            res = self.env['hr.contract'].search([])
            print("res >>>>>>>>>", res)
            for cu in res:
                all_employee_insurance.append(
                    {'employee_name': cu.employee_id.name, 'department': cu.department_id.name,
                     'job_position': cu.job_id.name, 'insurance_date': cu.insurance_date,
                     'insurance_salary': cu.insurance_salary, 'employee_percentage': cu.employee_percentage,
                     'company_percentage': cu.company_percentage, 'employee_amount': cu.employee_amount,
                     'company_amount': cu.company_amount, 'medical_date': cu.medical_date,
                     'medical_insurance_employee': cu.medical_insurance_employee,
                     'medical_insurance_family': cu.medical_insurance_family, })


                print("all_employee_insurance >>>>>>>>>", all_employee_insurance)

        if report_for == '2':
            print("2222222222222222222222222222")
            emp_list = self.env['hr.employee'].search([('id', 'in', employee_ids.ids)])
            print("emp_list >>>>>>>>>", emp_list)

            if emp_list:
                print("ahmed saber")

                for employee in emp_list:

                    res = self.env['hr.contract'].search([('employee_id', '=', employee.id)], )
                    all_contract = self.env['hr.contract'].search([])

                    print("all_contract ###############", all_contract)

                    for cu in res:
                        all_employee_insurance.append(
                            {'employee_name': cu.employee_id.name, 'department': cu.department_id.name,
                             'job_position': cu.job_id.name, 'insurance_date': cu.insurance_date,
                             'insurance_salary': cu.insurance_salary, 'employee_percentage': cu.employee_percentage,
                             'company_percentage': cu.company_percentage, 'employee_amount': cu.employee_amount,
                             'company_amount': cu.company_amount, 'medical_date': cu.medical_date,
                             'medical_insurance_employee': cu.medical_insurance_employee,
                             'medical_insurance_family': cu.medical_insurance_family, })
                print("res", res)

        print("all_employee_insurance >>>>", all_employee_insurance)

        docargs = {
            'doc_ids': docids,
            'doc_model': check_report.model,
            'name': data.get('name'),
            'emp': data.get('emp'),
            'all_employee_insurance': all_employee_insurance,
        }

        return docargs
