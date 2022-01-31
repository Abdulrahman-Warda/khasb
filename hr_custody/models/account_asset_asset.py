# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError

class AccountAsset(models.Model):
    _inherit = 'account.asset.asset'

    brand = fields.Char()
    barcode = fields.Char()
    model = fields.Char()
    place = fields.Char()
    serial_number = fields.Char()
