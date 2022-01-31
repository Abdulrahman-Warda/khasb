from odoo import api, models, _

class khasp_SalaryAdv_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.employee_insurance_report'

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
        print("list",list)
        for l in list:
            contracts.append({
                'name':l.employee_id.name,
                'wage':l.wage,
                'housing_allowances':l.house_allow,
                'employee_amount': l.ded_employee_gosi,
                'company_amount':l.ded_company_gosi,
                'total_amount':l.ded_gosi,


            })
        print('contracts',contracts)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'contracts': contracts,
        }

