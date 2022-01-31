# -*- coding: utf-8 -*-
from odoo import http

# class ProductTemplateKhasp(http.Controller):
#     @http.route('/product_template_khasp/product_template_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_template_khasp/product_template_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_template_khasp.listing', {
#             'root': '/product_template_khasp/product_template_khasp',
#             'objects': http.request.env['product_template_khasp.product_template_khasp'].search([]),
#         })

#     @http.route('/product_template_khasp/product_template_khasp/objects/<model("product_template_khasp.product_template_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_template_khasp.object', {
#             'object': obj
#         })