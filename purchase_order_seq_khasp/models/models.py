# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = (self.env['ir.sequence'].next_by_code('purchase.order.new')) or _('New')
    #     result = super(PurchaseOrderInherit, self).create(vals)
    #     return result

    # ممكن اضيف فيلد واعمل وراثة ليه واخترا اسم الشركة واضيفه فى ال sequence
    # company_id = fields.Many2one(
    #     comodel_name='res.company',
    #     required=True,
    #     ondelete='cascade'
    # )
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].with_context(force_company=company_id).next_by_code('purchase.order.new') or '/'
        return super(PurchaseOrderInherit, self.with_context(company_id=company_id)).create(vals)









# @api.model
# def create(self, vals):
#     if vals.get('name', 'New') == 'New' and vals.get('voucher_type') == 'receipt_voucher':
#         vals['name'] = (self.env['ir.sequence'].next_by_code('account.voucher.account.receipt')) or 'New'
#     return super(AccountVoucherAccount, self).create(vals)
#
# def create(self, vals):
#         if vals.get('name_seq', _('New')) == _('New'):
#             vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
#         result = super(HospitalPatient, self).create(vals)
#         return result
#
#     def _default_currency_id(self):
#         company_id = self.env.context.get('force_company') or self.env.context.get('company_id') or self.env.user.company_id.id
#         return self.env['res.company'].browse(company_id).currency_id
#
#     company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id.id)
#
#
# @api.model
# def create(self, vals):
#     company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
#     if vals.get('name', 'New') == 'New':
#         vals['name'] = self.env['ir.sequence'].with_context(force_company=company_id).next_by_code('purchase.order') or '/'
#     return super(PurchaseOrder, self.with_context(company_id=company_id)).create(vals)


