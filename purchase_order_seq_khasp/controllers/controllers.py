# -*- coding: utf-8 -*-
from odoo import http

# class PurchaseOrderSeqKhasp(http.Controller):
#     @http.route('/purchase_order_seq_khasp/purchase_order_seq_khasp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_seq_khasp/purchase_order_seq_khasp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_seq_khasp.listing', {
#             'root': '/purchase_order_seq_khasp/purchase_order_seq_khasp',
#             'objects': http.request.env['purchase_order_seq_khasp.purchase_order_seq_khasp'].search([]),
#         })

#     @http.route('/purchase_order_seq_khasp/purchase_order_seq_khasp/objects/<model("purchase_order_seq_khasp.purchase_order_seq_khasp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_seq_khasp.object', {
#             'object': obj
#         })