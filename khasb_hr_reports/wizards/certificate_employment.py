# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EmployeeTitlesReportWizard(models.TransientModel):
    _name = "certificate.report"
    _description = "Employee Certificate Report wizard"

    report_language = fields.Selection([
        ('en', 'English'),
        ('ar', 'Arabic'),
    ], string='Language', default='en', required=True)

    report_salary = fields.Boolean(string='Show Salary')
    employee_id = fields.Many2one(
        'hr.employee', readonly=False,
        default=lambda self: self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1),
    )
    def _calc_is_manager(self):
        if self.env.user.has_group('hr.group_hr_manager'):
            return True
        else:
           return False

    is_manager = fields.Boolean(default=lambda self:self._calc_is_manager())


    @api.multi
    def preview_report(self):
        data = {}
        data['employee_id'] = self.employee_id.id
        data['report_language'] = self.report_language
        data['report_salary'] = self.report_salary
        return self.env.ref('khasb_hr_reports.action_certificate_report_pdf').report_action(self, data=data, config=False)

