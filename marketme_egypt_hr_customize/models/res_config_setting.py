from odoo import models, fields, api, _, exceptions


class ConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    create_auto_holiday_allocation = fields.Boolean()

    def set_values(self):
        self.env['ir.config_parameter'].set_param("create_auto_holiday_allocation", self.create_auto_holiday_allocation )
        return super(ConfigSetting, self).set_values()

    @api.model
    def get_values(self):
        res = super(ConfigSetting, self).get_values()
        res['create_auto_holiday_allocation'] = (self.env['ir.config_parameter'].sudo().get_param('create_auto_holiday_allocation', default=False))
        return res

