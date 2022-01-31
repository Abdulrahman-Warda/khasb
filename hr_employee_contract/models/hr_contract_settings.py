# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HRContractSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    num_months = fields.Integer('Pre Ending Date Months To Notify')
    trial_num_months = fields.Integer('Pre Trial Ending Date Months To Notify')

    def set_values(self):
        res = super(HRContractSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('hr_request.num_months',
                                                  self.num_months)

        self.env['ir.config_parameter'].set_param('hr_request.trial_num_months',
                                                  self.trial_num_months)
        return res

    @api.model
    def get_values(self):
        res = super(HRContractSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        num_monthss = ICPSudo.get_param('hr_request.num_months')
        num_monthsss = int(num_monthss)

        trial_num_monthss = ICPSudo.get_param('hr_request.trial_num_months')
        trial_num_monthsss = int(trial_num_monthss)

        res.update(
            num_months=num_monthsss,
            trial_num_months=trial_num_monthsss,
        )
        return res
