# -*- coding: utf-8 -*-
from odoo import http

# class AccountingKhasp(http.Controller):
#     @http.route('/accounting_khasp/accounting_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accounting_khasp/accounting_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accounting_khasp.listing', {
#             'root': '/accounting_khasp/accounting_khasp',
#             'objects': http.request.env['accounting_khasp.accounting_khasp'].search([]),
#         })

#     @http.route('/accounting_khasp/accounting_khasp/objects/<model("accounting_khasp.accounting_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accounting_khasp.object', {
#             'object': obj
#         })