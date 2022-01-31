# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_contract_trial_wizard(models.TransientModel):
    _name = 'contract.trial.wizard'

    type = fields.Selection(string="Type", selection=[('employee', 'By Employee'), ('department', 'By Department'), ], default='employee', )
    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False, )


    def print_report(self):
        data = {
            'model': 'contract.trial.wizard',
            'form': self.read(['employee_id','type','department_id'])[0]
        }
        print('data',self.read(['employee_id','type','department_id']))
        return self.env.ref('khasp_hr_wizard_reports.contract_trial_report_tag').report_action(self, data=data, config=False)




