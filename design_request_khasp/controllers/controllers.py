# -*- coding: utf-8 -*-
from odoo import http

# class DesignRequestKhasp(http.Controller):
#     @http.route('/design_request_khasp/design_request_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/design_request_khasp/design_request_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('design_request_khasp.listing', {
#             'root': '/design_request_khasp/design_request_khasp',
#             'objects': http.request.env['design_request_khasp.design_request_khasp'].search([]),
#         })

#     @http.route('/design_request_khasp/design_request_khasp/objects/<model("design_request_khasp.design_request_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('design_request_khasp.object', {
#             'object': obj
#         })