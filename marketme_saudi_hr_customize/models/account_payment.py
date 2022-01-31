""" Initialize Account Payment """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountPayment(models.Model):
    """
        Inherit Account Payment:
         -
    """
    _inherit = 'account.payment'

    is_ticket = fields.Boolean()
    is_overtime = fields.Boolean()
    is_travel_allowances = fields.Boolean()

    # def post(self):
    #     """ Override write """
    #     # vals ={'field': value}  -> dectionary contains only new filled fields
    #     # self = Old valus
    #     # res =
    #     if self.is_ticket:
    #         bank_and_cash = self.env.ref('account.data_account_type_revenue')
    #         travel_ticket_account_id = self.env['ir.config_parameter'].sudo().get_param('travel_ticket_account_id')
    #
    #     for line in self.move_line_ids:
    #         if line.account_id.user_type_id not in bank_and_cash:
    #             line.update({
    #                 'account_id': int(travel_ticket_account_id)
    #             })
    #             return super(AccountPayment, self).post()
