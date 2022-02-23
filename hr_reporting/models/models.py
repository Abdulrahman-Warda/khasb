# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Department(models.Model):
    _inherit = 'hr.department'

    is_hr_department = fields.Boolean()

class Employee(models.Model):
    _inherit = 'hr.employee'

    embassy = fields.Many2one('res.country')
    national_id_iqama = fields.Char()
    employee_number = fields.Char()

class LetterConfig(models.Model):
    _name = 'letter.config'

    name = fields.Char()
    name_arabic = fields.Char()
    position = fields.Char()
    position_arabic = fields.Char()
    department = fields.Char()
    department_arabic = fields.Char()
    image = fields.Binary()
    definition_of_embassy = fields.Boolean()
    definition_of_salary_english = fields.Boolean()
    definition_wo_salary_english = fields.Boolean()
    definition_of_salary_arabic = fields.Boolean()
    definition_wo_salary_arabic = fields.Boolean()
