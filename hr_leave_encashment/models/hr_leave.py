import logging
import math

from collections import namedtuple

from datetime import datetime, time
from pytz import timezone, UTC

from odoo import api, fields, models
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_round
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period')

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    is_encashmented = fields.Boolean(default=False)
    # is_encashment_leave = fields.Boolean(default=False)
    # def activity_update(self):
    #     to_clean, to_do = self.env['hr.leave'], self.env['hr.leave']
    #     for holiday in self:
    #         if holiday.is_encashment_leave:
    #             pass
    #         else:
    #             start = UTC.localize(holiday.date_from).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
    #             end = UTC.localize(holiday.date_to).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
    #             note = _('New %s Request created by %s from %s to %s') % (holiday.holiday_status_id.name, holiday.create_uid.name, start, end)
    #             if holiday.state == 'draft':
    #                 to_clean |= holiday
    #             elif holiday.state == 'confirm':
    #                 holiday.activity_schedule(
    #                     'hr_holidays.mail_act_leave_approval',
    #                     note=note,
    #                     user_id=holiday.sudo()._get_responsible_for_approval().id or self.env.user.id)
    #             elif holiday.state == 'validate1':
    #                 holiday.activity_feedback(['hr_holidays.mail_act_leave_approval'])
    #                 holiday.activity_schedule(
    #                     'hr_holidays.mail_act_leave_second_approval',
    #                     note=note,
    #                     user_id=holiday.sudo()._get_responsible_for_approval().id or self.env.user.id)
    #             elif holiday.state == 'validate':
    #                 to_do |= holiday
    #             elif holiday.state == 'refuse':
    #                 to_clean |= holiday
    #     if to_clean:
    #         to_clean.activity_unlink(['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])
    #     if to_do:
    #         to_do.activity_feedback(['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])
