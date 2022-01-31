from odoo import models, fields, api, _, exceptions


class ConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    permission_type = fields.Selection(
        [('monthly', 'Monthly'),
         ('annual', 'Annual'),
         ('no_limit', 'No Limit')],
        default='no_limit',
    )
    permission_no = fields.Char()
    business_trip_account_id = fields.Many2one(
        'account.account'
    )
    travel_ticket_account_id = fields.Many2one(
        'account.account'
    )
    overtime_account_id = fields.Many2one(
        'account.account'
    )
    regular_day_rate = fields.Char()
    leave_day_rate = fields.Char()

    def set_values(self):
        self.env['ir.config_parameter'].set_param("permission_type", self.permission_type )
        self.env['ir.config_parameter'].set_param("permission_no", self.permission_no )
        self.env['ir.config_parameter'].set_param("business_trip_account_id", self.business_trip_account_id.id)
        self.env['ir.config_parameter'].set_param("travel_ticket_account_id", self.travel_ticket_account_id.id)
        self.env['ir.config_parameter'].set_param("overtime_account_id", self.overtime_account_id.id)
        self.env['ir.config_parameter'].set_param("regular_day_rate", self.regular_day_rate )
        self.env['ir.config_parameter'].set_param("leave_day_rate", self.leave_day_rate )
        return super(ConfigSetting, self).set_values()

    @api.model
    def get_values(self):
        res = super(ConfigSetting, self).get_values()
        res['permission_type'] = (self.env['ir.config_parameter'].sudo().get_param('permission_type', default='no_limit'))
        res['permission_no'] = (self.env['ir.config_parameter'].sudo().get_param('permission_no', default=0))
        res['business_trip_account_id'] = int((self.env['ir.config_parameter'].sudo().get_param('business_trip_account_id')))
        res['travel_ticket_account_id'] = int((self.env['ir.config_parameter'].sudo().get_param('travel_ticket_account_id')))
        res['overtime_account_id'] = int((self.env['ir.config_parameter'].sudo().get_param('overtime_account_id')))
        res['regular_day_rate'] = (self.env['ir.config_parameter'].sudo().get_param('regular_day_rate'))
        res['leave_day_rate'] = (self.env['ir.config_parameter'].sudo().get_param('leave_day_rate'))
        return res

