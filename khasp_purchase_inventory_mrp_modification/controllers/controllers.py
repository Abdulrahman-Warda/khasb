# -*- coding: utf-8 -*-
from odoo import http

# class KhaspPurchaseInventoryOrpModification(http.Controller):
#     @http.route('/khasp_purchase_inventory_orp_modification/khasp_purchase_inventory_orp_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/khasp_purchase_inventory_orp_modification/khasp_purchase_inventory_orp_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('khasp_purchase_inventory_orp_modification.listing', {
#             'root': '/khasp_purchase_inventory_orp_modification/khasp_purchase_inventory_orp_modification',
#             'objects': http.request.env['khasp_purchase_inventory_orp_modification.khasp_purchase_inventory_orp_modification'].search([]),
#         })

#     @http.route('/khasp_purchase_inventory_orp_modification/khasp_purchase_inventory_orp_modification/objects/<model("khasp_purchase_inventory_orp_modification.khasp_purchase_inventory_orp_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('khasp_purchase_inventory_orp_modification.object', {
#             'object': obj
#         })