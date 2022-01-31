# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit='project.project'

    employe_ids = fields.Many2many(comodel_name="hr.employee")
    employe_count = fields.Integer(string="Employees",compute='_calc_employe_count',store=True)
    date_start = fields.Date(string="Start Date", required=False)
    date_end = fields.Date(string="End Date", required=False)


    def renew_contract(self):
        if self.date_start and self.date_end:
            for employee in self.employe_ids:
                res=self.env['hr.contract'].search([('employee_id','=',employee.id),
                                                    ('date_start','=',str(self.date_start))
                                                       ,('date_end','=',str(self.date_end))
                                                       ,('project_id','=',self.id)
                                                    ])
                if not res:
                    vaules={
                        'project_id':self.id,
                        'name':str(employee.name)+"-"+str(self.date_start)+"-"+str(self.date_end),
                        'employee_id':employee.id,
                        'type_id':self.env.ref('hr_contract.hr_contract_type_emp').id,
                        'resource_calendar_id':self.env.ref('resource.resource_calendar_std').id,
                        'struct_id':self.env.ref('hr_payroll.structure_base').id,
                        'date_start':self.date_start,
                        'date_end':self.date_end,
                        'wage':0.0,
                        'state':'open'
                    }
                    self.env['hr.contract'].create(vaules)
        else:
            raise ValidationError("Start Date And End Date Required")


    @api.one
    @api.depends('employe_ids')
    def _calc_employe_count(self):
        self.employe_count=len(self.employe_ids.ids)

    def view_employees(self):
        action = self.env.ref('hr.open_view_employee_list_my').read()[0]
        action['domain']=[('id','in',self.employe_ids.ids)]
        return action