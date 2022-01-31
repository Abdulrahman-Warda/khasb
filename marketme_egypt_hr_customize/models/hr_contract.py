""" Initialize Hr Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrContract(models.Model):
    """
        Inherit Hr Contract:
         - 
    """
    _inherit = 'hr.contract'
    
    transport_allowances = fields.Float()
    living_allowances = fields.Float()
    other_allowances = fields.Float()
    internal_travel_allowances = fields.Float()
    abroad_travel_allowances = fields.Float()
    other_travel_allowances = fields.Float()
    hour_travel_allowances = fields.Float()
    general_deductions = fields.Float()
    regular_leave = fields.Float(
        compute='_compute_regular_leave'
    )
    emergency_leave = fields.Float(
        compute='_compute_emergency_leave'
    )
    hiring_date = fields.Date()
    allocation = fields.Boolean(
        compute='_compute_regular_leave'
    )

    def _compute_emergency_leave(self):
        """ Compute emergency_leave value """
        for rec in self:
            allocation = self.env['ir.config_parameter'].sudo().get_param('create_auto_holiday_allocation')
            if allocation:
                rec.emergency_leave = 6
            else:
                rec.emergency_leave = 0

    @api.depends('hiring_date', 'employee_id')
    def _compute_regular_leave(self):
        """ Compute regular_leave value """
        for rec in self:
            rec.allocation = self.env['ir.config_parameter'].sudo().get_param('create_auto_holiday_allocation')
            if rec.hiring_date and rec.allocation:
                time_difference = relativedelta(fields.Date.today(), rec.hiring_date)
                years = time_difference.years
                if years >= 1 and years <= 10:
                    rec.regular_leave = 15
                if years >= 10:
                    rec.regular_leave = 24
            else:
                rec.regular_leave = 0

    def create_leave_allocation(self):
        """ Create Notification """
        if self.env['ir.config_parameter'].sudo().get_param('create_auto_holiday_allocation'):
            today = fields.Date.today()
            contracts = self.search([
                ('state', '=', 'open'),
                ('regular_leave', '>', 0),
            ])
            regular = self.env.ref('marketme_egypt_hr_customize.regular_leave')
            emergency = self.env.ref('marketme_egypt_hr_customize.emergency_leave')
            allocation = self.env['hr.leave.allocation']
            for rec in contracts:
                allocation.create({
                    'name': rec.employee_id.name + ' Regular Allocation',
                    'employee_id': rec.employee_id.id,
                    'holiday_type': 'employee',
                    'holiday_status_id': regular.id,
                    'number_of_days': rec.regular_leave,
                })
                allocation.create({
                    'name': rec.employee_id.name + ' Emergency Allocation',
                    'employee_id': rec.employee_id.id,
                    'holiday_type': 'employee',
                    'holiday_status_id': emergency.id,
                    'number_of_days': rec.emergency_leave,
                })
