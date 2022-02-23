# -*- coding: utf-8 -*-

from odoo import models, fields, api

class emabssy_report_wizard(models.TransientModel):
    _name = 'embassy.report.wizard'

    embassy = fields.Many2one('res.country')

    def print_report(self):
        emp=self.env['hr.employee'].browse(self._context.get('active_id'))
        emp.write({'embassy':self.embassy.id})
        return self.env.ref('hr_reporting.action_report_definition_of_embassy').report_action(emp)
