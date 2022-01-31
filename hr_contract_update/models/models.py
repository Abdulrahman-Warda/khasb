# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    annual_leave_balance = fields.Integer(string="Annual leave balance", required=False, )
    @api.constrains('date_start', 'trial_date_end')
    def _check_contract_trial_period(self):
        """
        Contract Trial Period Cannot be More Than 3 Months
        """
        if self.date_start and self.trial_date_end:
            months = (self.trial_date_end.year - self.date_start.year) * 12 + self.trial_date_end.month - self.date_start.month
            if months > 3:
                raise ValidationError(_("Sorry, Trial Period Cannot be More Than 3 Months...."))
            else:
                return
