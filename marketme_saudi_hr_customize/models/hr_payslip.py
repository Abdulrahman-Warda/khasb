""" Initialize Hr Payslip """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrPayslip(models.Model):
    """
        Inherit Hr Payslip:
         -
    """
    _inherit = 'hr.payslip'

    travel_amount = fields.Float(
        compute='_compute_travel_amount'
    )
    overtime_amount = fields.Float(
        compute='_compute_overtime_amount'
    )

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_travel_amount(self):
        """ Compute _award_amount value """
        for rec in self:
            travel = rec.env['travel.allowances'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date_from', '>=', rec.date_from),
                ('date_from', '<=', rec.date_to),
                ('state', '=', 'approve'),
                ('payslip', '=', True)
            ])
            rec.travel_amount = sum(travel.mapped('amount'))

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_overtime_amount(self):
        """ Compute _award_amount value """
        for rec in self:
            overtime = rec.env['hr.overtime'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('overtime_date', '>=', rec.date_from),
                ('overtime_date', '<=', rec.date_to),
                ('state', '=', 'approve'),
                ('payslip', '=', True)
            ])
            rec.overtime_amount = sum(overtime.mapped('overtime_amount'))
