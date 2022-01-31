# -*- coding: utf-8 -*-
from odoo import http

# class ContractTracking(http.Controller):
#     @http.route('/contract_tracking/contract_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contract_tracking/contract_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('contract_tracking.listing', {
#             'root': '/contract_tracking/contract_tracking',
#             'objects': http.request.env['contract_tracking.contract_tracking'].search([]),
#         })

#     @http.route('/contract_tracking/contract_tracking/objects/<model("contract_tracking.contract_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contract_tracking.object', {
#             'object': obj
#         })