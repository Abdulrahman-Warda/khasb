# -*- coding: utf-8 -*-
from odoo import http

# class InspectionChecklistKhasp(http.Controller):
#     @http.route('/inspection_checklist_khasp/inspection_checklist_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inspection_checklist_khasp/inspection_checklist_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inspection_checklist_khasp.listing', {
#             'root': '/inspection_checklist_khasp/inspection_checklist_khasp',
#             'objects': http.request.env['inspection_checklist_khasp.inspection_checklist_khasp'].search([]),
#         })

#     @http.route('/inspection_checklist_khasp/inspection_checklist_khasp/objects/<model("inspection_checklist_khasp.inspection_checklist_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inspection_checklist_khasp.object', {
#             'object': obj
#         })