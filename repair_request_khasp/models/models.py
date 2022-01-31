# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime, date


class RepairRequest(models.Model):
    _name = 'repair.request'

    # States buttons functions
    def action_approval(self):
        for rec in self:
            rec.state = 'request to approval'

    def action_done(self):
        for rec in self:
            rec.state = 'done'



    # model's fields
    employee_name = fields.Many2one("hr.employee", string="Employee Name")
    employee_number = fields.Char(related="employee_name.mobile_phone", string="Employee Number")
    department_name = fields.Many2one("hr.department",related="employee_name.department_id", string="Department")
    supervisor_name = fields.Many2one("hr.employee",related="employee_name.parent_id", string="Supervisor Name")
    machine_name = fields.Many2one("mrp.workcenter", string="Machine Name")
    machine_number = fields.Char(related="machine_name.code", string="Machine Number")
    request_date = fields.Date(string="Request Date")
    request_time = fields.Datetime(string="Request Time")

    shift = fields.Selection([
        ('am', 'AM'),
        ('afternoon', 'Afternoon'),
        ('pm', 'PM')], string='Shift', default="am")

    start_Date = fields.Date(string="starting date")
    end_date = fields.Datetime(string="Finishing time")
    description_of_maintenance = fields.Text(string="Description of maintenance or inspection required:")

    type_of_maintenance = fields.Selection([
        ('pM', 'PM'),
        ('cM', 'CM'),
        ('emergency', 'Emergency'),
        ('maintenance', 'Development maintenance')], string='Type of maintenance', default="pM")

    repair_need = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Has the supervisor in that area been notified of the maintenance or repair need?')

    urgent_repair = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Is this repair request URGENT?')

    safety_concern = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Is the maintenance or repair request due to an accident or safety concern?')

    employee_signature = fields.Char(string="Employee Signature")
    report_date = fields.Date(string="Report Date", default=fields.Date.context_today, readonly=True)

    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('request to approval', 'Request To Approval'),
        ('done', 'Done')], string='Status', default="draft", readonly=True)



