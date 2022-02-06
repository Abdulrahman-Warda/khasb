# -*- coding: utf-8 -*-

from odoo import models, fields, api

class khasp_stock_move(models.Model):
    _inherit = 'stock.move'
    lot_serial_prefix = fields.Char()
    lot_serial_initial_number = fields.Integer()

    def update_serial_lot_lines(self):
        lot_serial_initial_number = self.lot_serial_initial_number
        for ml in self.move_line_ids:
            ml.lot_name = self.lot_serial_prefix + '/' + str(lot_serial_initial_number)
            lot_serial_initial_number += 1
            if ml.product_id.tracking != 'none':
                ml.qty_done = ml.product_uom_qty

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

    def set_quality_control(self):
        self.state = 'quality_control'
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
