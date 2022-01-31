# -*- coding: utf-8 -*-

from odoo import models, fields, api
class khasp_inventory_modification(models.Model):
    _inherit = 'stock.picking'
    state = fields.Selection([
        ('draft', 'Draft'),
        ('quality_control', 'Quality Control'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('qc_rejection', 'QC Rejection'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore.")


    @api.multi
    def action_confirm(self):
        res = super(khasp_inventory_modification, self).action_confirm()
        for rec in self:
            rec.state = 'quality_control'
        return res
class ReturnPickingModification(models.TransientModel):
    _inherit = 'stock.return.picking'

    def create_returns(self):
        res = super(ReturnPickingModification, self).create_returns()
        for rec in self:
            rec.picking_id.state='quality_control'
        return res