from odoo import api, models,fields, _
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

class khasp_Employee_joining_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.contract_date_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        department=docs.department_id
        type=docs.type
        contracts=[]
        if type == 'employee':
            list = self.env['hr.contract'].search([('state','=','open')])
        elif type == 'department':
            if department:
                list = self.env['hr.contract'].search([('department_id','=',department.id),('state','=','open')])
            else:
                list = self.env['hr.contract'].search([('state','=','open')])
        for l in list:

            contracts.append({
                'name':l.employee_id.name,
                'amount': l.date_start,
                'amount_end': l.date_end,
            })

        print('contracts',contracts)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'contracts': contracts,
        }

