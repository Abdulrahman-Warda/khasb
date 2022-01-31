from odoo import api, models,fields, _
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

class khasp_Employee_penalty_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.employee_penalty_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        department=docs.department_id
        type=docs.type
        contracts=[]
        if type == 'employee':
            list = self.env['hr.penalty'].search([('state','=','confirm')])
        elif type == 'department':
            if department:
                list = self.env['hr.penalty'].search([('department_id','=',department.id),('state','=','confirm')])
            else:
                list = self.env['hr.penalty'].search([('state','=','confirm')])
        for l in list:

            contracts.append({
                'name':l.employee_id.name,
                'amount_date': l.date,
                'amount_type': l.penalty_type,
                'amount_value': l.total_amount,
            })

        print('contracts',contracts)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'contracts': contracts,
        }

