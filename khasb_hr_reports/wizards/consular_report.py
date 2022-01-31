# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EmployeeConsularWizard(models.TransientModel):
    _name = "consular.report"
    _description = "Employee consular Report wizard"

    country = fields.Many2one('res.country', string='Embassy', required=1)
    employee_id = fields.Many2one(
        'hr.employee', readonly=0,
        default=lambda self: self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1),
    )

    def _calc_is_manager(self):
        if self.env.user.has_group('hr.group_hr_manager'):
            return True
        else:
            return False

    is_manager = fields.Boolean(default=lambda self: self._calc_is_manager())


    @api.multi
    def preview_report(self):
        data = {}
        data['employee_id'] = self.employee_id.id
        data['country'] = self.country.name
        return self.env.ref('khasb_hr_reports.action_consular_report_pdf').report_action(self, data=data, config=False)

