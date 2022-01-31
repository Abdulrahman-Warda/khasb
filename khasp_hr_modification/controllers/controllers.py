# -*- coding: utf-8 -*-
from odoo import http

# class KhaspHrModification(http.Controller):
#     @http.route('/khasp_hr_modification/khasp_hr_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/khasp_hr_modification/khasp_hr_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('khasp_hr_modification.listing', {
#             'root': '/khasp_hr_modification/khasp_hr_modification',
#             'objects': http.request.env['khasp_hr_modification.khasp_hr_modification'].search([]),
#         })

#     @http.route('/khasp_hr_modification/khasp_hr_modification/objects/<model("khasp_hr_modification.khasp_hr_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('khasp_hr_modification.object', {
#             'object': obj
#         })