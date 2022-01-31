from odoo import api, models, _

class khasp_SalaryAdv_report(models.AbstractModel):
    _name = 'report.khasp_hr_wizard_reports.salary_advance_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        employee = docs.employee_id
        salary_adv=[]
        if employee:
            lean = self.env['hr.loan'].search([('employee_id','=',employee.id),('state','=','confirm')])
        else:
            lean = self.env['hr.loan'].search([('state','=','confirm')], order='employee_id asc')
        for l in lean:
            salary_adv.append({
                'name':l.employee_id.name,
                'amount':l.balance_amount,
            })
        print('lean',lean)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'salary_list': salary_adv,
        }

