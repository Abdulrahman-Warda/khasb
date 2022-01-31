from odoo import api, models,fields, _
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

class khasp_Employee_age_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.employee_age_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        department=docs.department_id
        type=docs.type
        contracts=[]
        if type == 'employee':
            list = self.env['hr.employee'].search([])
        elif type == 'department':
            if department:
                list = self.env['hr.employee'].search([('department_id','=',department.id)])
            else:
                list = self.env['hr.employee'].search([])
        for l in list:
            if l.birthday:
                d1 = datetime.strptime(str(l.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                age = relativedelta(d2, d1).years
                contracts.append({
                    'name':l.name,
                    'amount': age,
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

