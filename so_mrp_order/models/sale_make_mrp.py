# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError


class So(models.Model):
    _inherit = 'sale.order'

    created_mrp = fields.Boolean(default=False, copy=False)
    tempreature = fields.Char('Tempreature')
    mrp_count = fields.Float(default=0.0, compute="_compute_mrp_count")

    def _compute_mrp_count(self):
        for this in self:
            this.mrp_count = self.env['mrp.production'].search_count([('origin','=',this.name)])

    def action_view_mrp(self):
        mrps = self.env['mrp.production'].search([('origin','=',self.name)])
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        action['domain'] = [('id', 'in', mrps.ids)]
        return action
    @api.multi
    def create_mrp(self):
        if self.env.user.has_group('so_mrp_order.group_create_mrp_from_so'):
            prods=[]
            for order in self:
                for line in order.order_line:
                    if line.product_id.to_make_mrp:
                        product_dict={
                            'id': line.product_id.id,
                            'qty': line.product_uom_qty,
                            'product_tmpl_id': line.product_id.product_tmpl_id.id,
                            'so_reference': order.name,
                            'uom_id': line.product_uom.id,
                            'tempreature': order.tempreature,
                            'customer': order.partner_id.id,
                            'company_id': order.company_id.id,
                       }
                        prods.append(product_dict)
                        print(product_dict)
            self.created_mrp = True
            return self.create_mrp_from_so(prods)
        else:
            raise ValidationError("ليس لديك صلاحية")

    @api.multi
    def create_mrp_from_so(self, products):
        product_ids = []
        mrps=[]
        if products:
            for product in products:
                flag = 1
                if product_ids:
                    for product_id in product_ids:
                        if product_id['id'] == product['id']:
                            product_id['qty'] += product['qty']
                            flag = 0
                if flag:
                    product_ids.append(product)
            for prod in product_ids:
                if prod['qty'] > 0:
                    print(prod)
                    product = self.env['product.product'].search([('id', '=', prod['id'])])
                    # bom_count = self.env['mrp.bom'].search([('product_tmpl_id', '=', prod['product_tmpl_id'])])
                    # if bom_count:
                    #     bom_temp = self.env['mrp.bom'].search([('product_tmpl_id', '=', prod['product_tmpl_id']),
                    #                                            ('product_id', '=', False)])
                    #     bom_prod = self.env['mrp.bom'].search([('product_id', '=', prod['id'])])
                    #     if bom_prod:
                    #         bom = bom_prod[0]
                    #     elif bom_temp:
                    #         bom = bom_temp[0]
                    #     else:
                    #         bom = []
                    #     if bom:
                    vals = {
                        'origin':prod['so_reference'],
                        'state': 'confirmed',
                        'product_id': prod['id'],
                        'product_tmpl_id': prod['product_tmpl_id'],
                        'product_uom_id': prod['uom_id'],
                        'product_qty': prod['qty'],
                        'bom_id': product.bom_ids[0].id,
                        'tempreature':prod['tempreature'],
                        'customer': prod['customer'],
                        'company_id': prod['company_id']
                    }
                    print(vals)
                    res=self.env['mrp.production'].sudo().create(vals)
                    print(res)
                    mrps.append(res.id)
        print(mrps)
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        action['domain'] = [('id', 'in', mrps)]
        return action


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    to_make_mrp = fields.Boolean(string='To Create MRP Order',
                                 help="Check if the product should be make mrp order")

    @api.onchange('to_make_mrp')
    def onchange_to_make_mrp(self):
        if self.to_make_mrp:
            if not self.bom_count:
                raise Warning('Please set Bill of Material for this product.')


class ProductProduct(models.Model):
    _inherit = 'product.product'
    to_make_mrp = fields.Boolean(string='To Create MRP Order',
                                 help="Check if the product should be make mrp order",related='product_tmpl_id.to_make_mrp',store=True,readonly=False)

    @api.onchange('to_make_mrp')
    def onchange_to_make_mrp(self):
        if self.to_make_mrp:
            if not self.bom_count:
                raise Warning('Please set Bill of Material for this product.')
