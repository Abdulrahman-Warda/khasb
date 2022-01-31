# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ToolInspection(models.Model):
    _name = 'tool.inspection'

    # model's fields
    tool_name = fields.Many2one("product.template", string="Tool Name")
    tool_number = fields.Char(related="tool_name.prod_number",
                                      string="Tool Number", readonly=True, required=False)

    calibration_date = fields.Date(string="Calibration Date")
    calibration_expiry_date = fields.Date(string="Calibration Expiry Date")
    accuracy = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Accuracy')
    remarks = fields.Text(string="Remarks")
