# -*- coding: utf-8 -*-
from odoo import http

# class KhaspSaleManificatureReports(http.Controller):
#     @http.route('/khasp_sale_manificature_reports/khasp_sale_manificature_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/khasp_sale_manificature_reports/khasp_sale_manificature_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('khasp_sale_manificature_reports.listing', {
#             'root': '/khasp_sale_manificature_reports/khasp_sale_manificature_reports',
#             'objects': http.request.env['khasp_sale_manificature_reports.khasp_sale_manificature_reports'].search([]),
#         })

#     @http.route('/khasp_sale_manificature_reports/khasp_sale_manificature_reports/objects/<model("khasp_sale_manificature_reports.khasp_sale_manificature_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('khasp_sale_manificature_reports.object', {
#             'object': obj
#         })