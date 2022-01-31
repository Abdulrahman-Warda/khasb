from odoo import api, models,fields, _
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

class khasp_Employee_joining_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.employee_joining_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        department=docs.department_id
        type=docs.type
        contracts=[]
        if type == 'employee':
            list = self.env['hr.employee'].search([],order='joining_date asc')
        elif type == 'department':
            if department:
                list = self.env['hr.employee'].search([('department_id','=',department.id)],order='joining_date asc')
            else:
                list = self.env['hr.employee'].search([],order='joining_date asc')
        for l in list:
            if l.joining_date:
                contracts.append({
                    'name':l.name,
                    'amount': l.joining_date,
                })
            else:
                contracts.append({
                    'name': l.name,
                    'amount': 'Not Inserted',
                })
        print('contracts',contracts)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'contracts': contracts,
        }

