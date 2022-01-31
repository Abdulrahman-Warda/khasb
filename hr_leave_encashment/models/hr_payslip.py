from datetime import datetime, time
from pytz import timezone, UTC
from odoo import api, fields, models
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_round
from odoo.tools.translate import _
class Payslip(models.Model):
    _inherit = "hr.payslip"

    total_encashment = fields.Float(compute="_compute_total_encashment")

    @api.onchange('employee_id', 'date_from', 'date_to')
    def _compute_total_encashment(self):
        for this in self:
            if this.employee_id and this.date_from and this.date_to:
                this.total_encashment = sum(self.env['hr.leave.encashment'].search([('payment_type','=','payslip_id'),('is_processed','=',True),('name','=',this.employee_id.id),('process_date','>=',this.date_from),('process_date','<=',this.date_to)]).mapped('total_encashment'))
            else:
                this.total_encashment = 0.0
