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
    award_amount = fields.Float(
        compute='_compute_award_amount'
    )
    penalty_amount = fields.Float(
        compute='_compute_penalty_amount'
    )

    transportation_amount = fields.Float(
        compute='_compute_transportation_amount'
    )

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_penalty_amount(self):
        """ Compute penalty_amount value """
        for rec in self:
            penalty = rec.env['hr.penalty'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('state', '=', 'confirm')
            ])
            rec.penalty_amount = sum(penalty.mapped('total_amount'))

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_transportation_amount(self):
        """ Compute penalty_amount value """
        for rec in self:
            transportation = rec.env['hr.transportation'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('state', '=', 'confirm')
            ])
            rec.transportation_amount = sum(transportation.mapped('amount'))

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_award_amount(self):
        """ Compute _award_amount value """
        for rec in self:
            award = rec.env['hr.award'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('state', '=', 'confirm')
            ])
            rec.award_amount = sum(award.mapped('total_amount'))

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_travel_amount(self):
        """ Compute _award_amount value """
        for rec in self:
            travel = rec.env['travel.allowances'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date_from', '>=', rec.date_from),
                ('date_from', '<=', rec.date_to),
                ('state', '=', 'confirm')
            ])
            rec.travel_amount = sum(travel.mapped('amount'))
