# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    termination_id = fields.Many2one(comodel_name="hr.termination", string="", required=False, )

