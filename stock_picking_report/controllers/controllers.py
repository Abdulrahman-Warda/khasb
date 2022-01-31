# -*- coding: utf-8 -*-
from odoo import http

# class StockPickingReport(http.Controller):
#     @http.route('/stock_picking_report/stock_picking_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_report/stock_picking_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_report.listing', {
#             'root': '/stock_picking_report/stock_picking_report',
#             'objects': http.request.env['stock_picking_report.stock_picking_report'].search([]),
#         })

#     @http.route('/stock_picking_report/stock_picking_report/objects/<model("stock_picking_report.stock_picking_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_report.object', {
#             'object': obj
#         })