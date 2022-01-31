# -*- coding: utf-8 -*-
from odoo import http

# class KhaspHrWizardReports(http.Controller):
#     @http.route('/khasp_hr_wizard_reports/khasp_hr_wizard_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/khasp_hr_wizard_reports/khasp_hr_wizard_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('khasp_hr_wizard_reports.listing', {
#             'root': '/khasp_hr_wizard_reports/khasp_hr_wizard_reports',
#             'objects': http.request.env['khasp_hr_wizard_reports.khasp_hr_wizard_reports'].search([]),
#         })

#     @http.route('/khasp_hr_wizard_reports/khasp_hr_wizard_reports/objects/<model("khasp_hr_wizard_reports.khasp_hr_wizard_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('khasp_hr_wizard_reports.object', {
#             'object': obj
#         })