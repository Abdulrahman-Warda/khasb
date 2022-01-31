from odoo import fields, models,api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Integer('Credit Limit')
    # remaining_limit = fields.Float('Remaining Limit',compute='_calc_remaining',store=True)

    # @api.one
    # @api.depends('credit_limit','invoice_ids')
    # def _calc_remaining(self):
    #     inv_total_amt = 0
    #     print("self.invoice_ids",self.invoice_ids)
    #     inv_rec = self.invoice_ids
    #     for inv in inv_rec:
    #         if inv not in ['draft', 'cancel']:
    #             inv_total_amt += inv.amount_total - inv.residual
    #     self.remaining_limit=self.credit_limit-inv_total_amt
