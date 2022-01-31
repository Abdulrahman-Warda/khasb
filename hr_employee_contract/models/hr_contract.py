# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Hr Contract'

    insurance_date = fields.Date()
    insurance_salary = fields.Float()
    employee_percentage = fields.Float()
    company_percentage = fields.Float()
    employee_amount = fields.Float(compute='get_employee_percentage')
    company_amount = fields.Float(compute='get_employee_percentage')

    medical_date = fields.Date()
    medical_insurance_employee = fields.Float()
    medical_insurance_family_check = fields.Boolean()
    medical_insurance_family = fields.Float()

    start_warning_end_date = fields.Date(compute='compute_start_warning_end_date',store=True)
    start_warning_end_trial_date = fields.Date(compute='compute_start_warning_end_date',store=True)
    link = fields.Char()
    project_id = fields.Many2one(comodel_name="project.project")


    @api.multi
    @api.depends('date_end','trial_date_end')
    def compute_start_warning_end_date(self):
        config = self.env['res.config.settings'].search([])
        if config:
            config = config[-1]
            for rec in self:
                if rec.date_end:
                    start_warning_end_date = rec.date_end - relativedelta(months=config.num_months)
                    rec.start_warning_end_date = start_warning_end_date
                if rec.trial_date_end:
                    start_warning_end_trial_date = rec.trial_date_end - relativedelta(months=config.trial_num_months)
                    rec.start_warning_end_trial_date = start_warning_end_trial_date

    @api.depends('employee_percentage', 'company_percentage')
    def get_employee_percentage(self):
        for rec in self:
            rec.employee_amount = rec.get_amount_insurance(rec.insurance_salary, rec.employee_percentage)
            rec.company_amount = rec.get_amount_insurance(rec.insurance_salary, rec.company_percentage)

    def get_amount_insurance(self,insurance_salary,insurance_percentage):
        return insurance_salary * (insurance_percentage / 100)

    @api.model
    def _cron_contract_ending(self):
        today_date = fields.Date.today()
        matched_contracts = self.search(
            [('date_end', '>=', today_date), ('start_warning_end_date', '<=', today_date), ('active', '=', True),
             ('state','!=','close')])
        for contract in matched_contracts:
            template_id = contract.env.ref('hr_employee_contract.mail_template_ending_contract_notify')
            action = contract.env.ref('hr_contract.action_hr_contract').id
            template_id.email_from = contract.company_id.email
            print('template_id',template_id.email_from)
            group_hr_officers = contract.env.ref('hr.group_hr_user').users
            for user in group_hr_officers:
                next_employee = contract.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
                print('next_employee',next_employee)
                if next_employee:
                    template_id.email_to = next_employee.work_email
                    if user.lang == 'en_US':
                        print('user.lang',user.lang)
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  Mr {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """
                                    Please Update Contract Employee <"a href="${object.employee_id.name}>
                                    <a href="${object.link}">From here</a>
                                </p>
                            </div>
                         """
                    elif user.lang == 'ar_AA':
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  السيد/ {name} </p>
                               <p>

                                    """.format(name=next_employee.name) + """
                                    من فضلك قم بتحديث عقد الموظف <a href="${object.employee_id.name}">
                                    <a href="${object.link}">من هنا</a>
                                </p>
                            </div>
                         """

    @api.model
    def _cron_contract_trial_ending(self):
        today_date = fields.Date.today()
        matched_contracts = self.search(
            [('trial_date_end', '>=', today_date), ('start_warning_end_trial_date', '<=', today_date), ('active', '=', True)])
        for contract in matched_contracts:
            template_id = contract.env.ref('hr_employee_contract.mail_template_trail_ending_contract_notify')
            action = contract.env.ref('hr_contract.action_hr_contract').id
            template_id.email_from = contract.company_id.email
            group_hr_officers = contract.env.ref('hr.group_hr_user').users
            for user in group_hr_officers:
                next_employee = contract.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
                if next_employee:
                    template_id.email_to = next_employee.work_email
                    print(user.lang)
                    if user.lang == 'ar_AA':
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  السيد/ {name} </p>
                               <p>

                                    """.format(name=next_employee.name) + """
                                    لقد شارفت المده التجريبيه للموظف يرجى أخذ إجراء للعقد <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">من هنا</a>
                                </p>
                            </div>
                         """
                    else:
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p> MR/ {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """The trial end date for employee <a 
                                    href="${object.employee_id.name}"/> comes soon so please tack action <a href="${
                                    object.link}">From Here</a> </p> </div> """
                    base = contract.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    base += "/web" + "/#id=%s&view_type=form&model=hr.contract&action=%s" % (contract.id, action)
                    contract.link = base
                    res = template_id.send_mail(contract.id, force_send=True)
                    print('***re`s', res)
