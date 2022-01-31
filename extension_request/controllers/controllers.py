# -*- coding: utf-8 -*-
# from odoo import http


# class ExtensionRequest(http.Controller):
#     @http.route('/extension_request/extension_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extension_request/extension_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extension_request.listing', {
#             'root': '/extension_request/extension_request',
#             'objects': http.request.env['extension_request.extension_request'].search([]),
#         })

#     @http.route('/extension_request/extension_request/objects/<model("extension_request.extension_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extension_request.object', {
#             'object': obj
#         })
