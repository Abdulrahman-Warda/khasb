# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DesignRequest(models.Model):
    _name = 'design.request'

    # model's fields
    quantity = fields.Text("Quantity of parts: (if there is more then 1 please specify)")
    design_specifications = fields.Text("Design specifications")
    usage_of_design = fields.Text("Usage of design:")
    tolerance_of_design = fields.Text("Tolerance of design")
    type_of_material = fields.Text("Type of material ( if available)")

    type_of_service = fields.Selection([
        ('new design', 'New design'),
        ('reverse engineer', 'Reverse engineer'),
        ('dimension matching', "Dimension's matching(CMM)"),
        ('lab material', 'Lab material analysis')], string='Type of service',)

    safety_requirements = fields.Selection([
        ('specificsafety', ' Is there specific safety standard'),
        ('other', 'Other'),
        ('requirements', 'No requirements')], string='Safety requirements', defualt='requirements')

    quantityParts = fields.Text(string="please specify……")

    material_treatments = fields.Selection([
        ('heat', 'Heat treatment'),
        ('paint', 'Paint'),
        ('sand', 'Sand blasting')], string='Material treatments')

    available_sample = fields.Selection(string="Available Sample", selection=[('yes', 'Yes'), ('no', 'No'), ], required=False)
