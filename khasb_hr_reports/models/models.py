# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Empoyee(models.Model):
    _inherit='hr.employee'
    cer_sequence = fields.Char(string="رقم الشهادة", required=False)
    arabic_name = fields.Char(string="الاسم بالعربي", required=False)
    joining_date = fields.Date(string="تاريخ الالتحاق", required=False)
