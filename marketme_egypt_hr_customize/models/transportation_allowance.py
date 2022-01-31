""" Initialize Hr award """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrTransportation(models.Model):
    """
        Initialize Hr transportation:
         -
    """
    _name = 'hr.transportation'
    _description = 'Hr Transportation'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_available_employee_ids(self):
        if self.env.user.has_group('marketme_egypt_hr_customize.group_allowance_and_deduction_own_document'):
            available_employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        elif self.env.user.has_group('marketme_egypt_hr_customize.group_allowance_and_deduction_department_document'):
            available_employee_ids = self.env['hr.employee'].search([('parent_id.user_id', '=', self.env.user.id)])
        else:
            available_employee_ids = self.env['hr.employee'].search([])
        return available_employee_ids

    employee_id = fields.Many2one(
        'hr.employee',
        track_visibility='onchange'
    )
    available_employee_ids = fields.Many2many(
        'hr.employee',
        default=lambda s: s._get_available_employee_ids(),
    )
    date = fields.Date(
        track_visibility='onchange'
    )
    amount = fields.Float(
        track_visibility='onchange'
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange'
    )
    notes = fields.Text(
        track_visibility='onchange'
    )

    # award_type = fields.Selection(string="Award Type",
    #                               selection=[('amount', 'Amount'), ('percent', 'Percent'), ('days', 'Days'), ],
    #                               required=False, )
    # days = fields.Integer(string="Days", required=False, )
    # percent = fields.Integer(string="Percent", required=False, )
    #
    # daily_wage = fields.Float(string="Daily Wage", required=False, )
    #
    # total_amount = fields.Float(string="",  required=False,)

    # @api.onchange('employee_id')
    # def _get_daily_wage(self):
    #     if self.employee_id:
    #         if self.employee_id.employee_work_type == 'office':
    #             self.daily_wage = self.employee_id.contract_id.wage / 22
    #         elif self.employee_id.employee_work_type == 'site':
    #             self.daily_wage = self.employee_id.contract_id.wage / 26
    #         else:
    #             self.daily_wage = 0.0
    #     else:
    #         self.daily_wage = 0.0

    # @api.onchange('employee_id', 'award_type', 'daily_wage', 'amount', 'percent', 'days')
    # def _get_total_amount(self):
    #     if self.employee_id and self.daily_wage and self.award_type:
    #         if self.award_type == 'amount':
    #             self.total_amount = self.amount
    #         elif self.award_type == 'percent':
    #             self.total_amount = self.daily_wage * self.percent
    #         elif self.award_type == 'days':
    #             self.total_amount = self.daily_wage * self.days
    #         else:
    #             self.total_amount = 0.0

    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'confirm'
            })

    def action_cancel(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'cancel'
            })

    def action_draft(self):
        """ Action Confirm """
        for rec in self:
            rec.write({
                'state': 'draft'
            })

