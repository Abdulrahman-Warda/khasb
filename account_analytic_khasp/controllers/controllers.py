# -*- coding: utf-8 -*-
from odoo import http

# class AccountAnalyticKahsp(http.Controller):
#     @http.route('/account_analytic_kahsp/account_analytic_kahsp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_analytic_kahsp/account_analytic_kahsp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_analytic_kahsp.listing', {
#             'root': '/account_analytic_kahsp/account_analytic_kahsp',
#             'objects': http.request.env['account_analytic_kahsp.account_analytic_kahsp'].search([]),
#         })

#     @http.route('/account_analytic_kahsp/account_analytic_kahsp/objects/<model("account_analytic_kahsp.account_analytic_kahsp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_analytic_kahsp.object', {
#             'object': obj
#         })