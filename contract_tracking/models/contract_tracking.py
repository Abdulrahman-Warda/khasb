# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class HrContract(models.Model):
    _inherit = 'hr.contract'

    pre_3mon_date = fields.Date(compute='compute_pre_3mon_date')
    link = fields.Char()

    def compute_pre_3mon_date(self):
        self.pre_3mon_date = self.date_end - relativedelta(months=2)

    @api.model
    def _cron_contract_ending(self):
        print('ahmed saber >>>>>>>>>>>>> _cron_contract_ending')
        today_date = fields.Date.today()
        print('today is: ', today_date)
        matched_contracts = self.search(
            [('date_end', '>=', today_date), ('pre_3mon_date', '<=', today_date), ('state', '=', 'open'),
             ('active', '=', True)])
        print(matched_contracts)
        for contract in matched_contracts:
            template_id = contract.env.ref('contract_tracking.mail_template_ending_contract_notify')
            action = contract.env.ref('hr_contract.action_hr_contract').id
            template_id.email_from = contract.company_id.email
            print("template_id.email_from",  template_id.email_from)
            group_hr_officers = contract.env.ref('hr.group_hr_user').users
            print("group_hr_officers", group_hr_officers)
            for user in group_hr_officers:
                next_employee = contract.env['hr.employee'].search([('id', '=', user.id)], limit=1)
                print("next_employee", next_employee)
                if next_employee:
                    template_id.email_to = next_employee.private_email
                    print(user.lang)
                    if user.lang != 'en_US':
                        print("1111")
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  السيد/ {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """
                                    من فضلك قم بتحديث عقد الموظف <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">من هنا</a>
                                </p>
                            </div>
                         """
                    else:
                        print("2222")
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p> MR/ {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """
                                    Please renew contract for employee <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">From Here</a>
                                </p>
                            </div>
                        """
                    base = contract.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    base += "/web" + "/#id=%s&view_type=form&model=hr.contract&action=%s" % (contract.id, action)
                    contract.link = base
                    res = template_id.send_mail(contract.id, force_send=True)
                    print('***res', res)



