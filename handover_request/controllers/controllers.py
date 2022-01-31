# -*- coding: utf-8 -*-
# from odoo import http


# class HandoverRequest(http.Controller):
#     @http.route('/handover_request/handover_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/handover_request/handover_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('handover_request.listing', {
#             'root': '/handover_request/handover_request',
#             'objects': http.request.env['handover_request.handover_request'].search([]),
#         })

#     @http.route('/handover_request/handover_request/objects/<model("handover_request.handover_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('handover_request.object', {
#             'object': obj
#         })
