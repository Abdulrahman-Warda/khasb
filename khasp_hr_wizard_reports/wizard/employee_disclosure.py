# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_employee_disclosure_wizard(models.TransientModel):
    _name = 'employee.salary.advance.wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    # type = fields.Selection(string="Type", selection=[('lean', 'Lean'), ('salary_advance', 'Salary Advance'), ], required=False, )


    def print_report(self):
        data = {
            'model': 'employee.salary.advance.wizard',
            'form': self.read(['employee_id'])[0]
        }
        print('data',self.read(['employee_id']))
        return self.env.ref('khasp_hr_wizard_reports.salary_advance_report_tag').report_action(self, data=data, config=False)




