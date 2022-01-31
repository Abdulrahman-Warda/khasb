# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_purchase_modification(models.Model):
    _inherit = 'purchase.order'
    state = fields.Selection([
        ('pre_draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('factory_manger', 'Factory Manger'),
        ('financial_manger', 'Financial Manger'),
        ('draft', 'General Manger'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')], string='Status', readonly=True, index=True, copy=False, default='pre_draft', track_visibility='onchange')
    is_quality_checked = fields.Boolean(compute="_compute_is_quality_checked_done")
    is_quality_checked_done = fields.Boolean(compute="_compute_is_quality_checked_done")
    def _compute_is_quality_checked_done(self):
        for this in self:
            this.is_quality_checked_done = True
            this.is_quality_checked = False
            if not this.picking_ids:
                this.is_quality_checked = False
            elif this.picking_ids:
                for pick in this.picking_ids:
                    if pick.state == 'done':
                        this.is_quality_checked = True
                        break
                    else:
                        this.is_quality_checked = False
            for line in this.order_line:
                if line.product_qty != line.qty_received:
                    this.is_quality_checked_done = False



    purchase_request_id = fields.Many2one(comodel_name="sprogroup.purchase.request", string="Purchase Request", required=False, )
    @api.multi
    def button_confirm(self):
        res = super(khasp_purchase_modification, self).button_confirm()
        for rec in self:
            stock=self.env['stock.picking'].search([('purchase_id','=',rec.id),('state', '=', 'assigned')])
            for s in stock:
                s.state='quality_control'

        return res

    @api.multi
    def button_draft(self):
        res = super(khasp_purchase_modification, self).button_draft()
        self.state='pre_draft'
        return res
    def check_amount_total(self):
        for rec in self:
            if rec.amount_total >= 1000 and rec.purchase_request_id.po_type=='private':
                rec.state ='factory_manger'
            elif rec.amount_total >= 1000 and rec.purchase_request_id.po_type!='private':
                rec.state = 'financial_manger'
            else:
                rec.state = 'draft'
                rec.button_confirm()

    def factory_manger_move(self):
        for rec in self:
            rec.state='financial_manger'

    def financial_manger_move(self):
        for rec in self:
            rec.state='draft'

    @api.multi
    def quality_action_view_picking(self):
        """ This function returns an action that display existing picking orders of given purchase order ids. When only one found, show the picking immediately.
        """
        for line in self.order_line:
            if line.product_qty != line.qty_received:
                line._create_or_update_picking()
        stock=self.env['stock.picking'].search([('purchase_id','=',self.id),('state', '=', 'assigned')])
        for s in stock:
            s.state='quality_control'
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        # override the context to get rid of the default filtering on operation type
        result['context'] = {}
        pick_ids = self.mapped('picking_ids')
        # choose the view_mode accordingly
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = pick_ids.id
        return result




class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    order_id = fields.Many2one('purchase.order','Order Reference')

    def _select(self):
        return super(PurchaseReport, self)._select() + ", l.order_id as order_id"

    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + ", l.order_id"
