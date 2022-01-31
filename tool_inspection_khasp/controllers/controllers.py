# -*- coding: utf-8 -*-
from odoo import http

# class ToolInspectionKhasp(http.Controller):
#     @http.route('/tool_inspection_khasp/tool_inspection_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tool_inspection_khasp/tool_inspection_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tool_inspection_khasp.listing', {
#             'root': '/tool_inspection_khasp/tool_inspection_khasp',
#             'objects': http.request.env['tool_inspection_khasp.tool_inspection_khasp'].search([]),
#         })

#     @http.route('/tool_inspection_khasp/tool_inspection_khasp/objects/<model("tool_inspection_khasp.tool_inspection_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tool_inspection_khasp.object', {
#             'object': obj
#         })