# -*- coding: utf-8 -*-
from odoo import http

# class RepairRequestKhasp(http.Controller):
#     @http.route('/repair_request_khasp/repair_request_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/repair_request_khasp/repair_request_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('repair_request_khasp.listing', {
#             'root': '/repair_request_khasp/repair_request_khasp',
#             'objects': http.request.env['repair_request_khasp.repair_request_khasp'].search([]),
#         })

#     @http.route('/repair_request_khasp/repair_request_khasp/objects/<model("repair_request_khasp.repair_request_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('repair_request_khasp.object', {
#             'object': obj
#         })