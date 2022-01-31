# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta, datetime
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError


class ReportEmployeecertificate(models.AbstractModel):
    _name = 'report.khasb_hr_reports.certificate_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.employee'].browse(data.get('employee_id'))

        docargs = {
            'docs': docs,
            'date': date.today(),
            'report_language': data.get('report_language'),
            'report_salary': data.get('report_salary'),
            'company': self.env.user.company_id,

        }

        return docargs
