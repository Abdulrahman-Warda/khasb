# -*- coding: utf-8 -*-
# from odoo import http


# class HrContractUpdate(http.Controller):
#     @http.route('/hr_contract_update/hr_contract_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_contract_update/hr_contract_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_contract_update.listing', {
#             'root': '/hr_contract_update/hr_contract_update',
#             'objects': http.request.env['hr_contract_update.hr_contract_update'].search([]),
#         })

#     @http.route('/hr_contract_update/hr_contract_update/objects/<model("hr_contract_update.hr_contract_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_contract_update.object', {
#             'object': obj
#         })
