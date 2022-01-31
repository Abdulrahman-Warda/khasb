# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.tools import float_compare, float_round, float_is_zero
from odoo.exceptions import ValidationError,UserError


class MrpOrder(models.Model):
    _inherit = 'mrp.production'
    routing_id2 = fields.Many2one(
        'mrp.routing', 'Routing',
        readonly=False,
        help="The list of operations (list of work centers) to produce the finished product. The routing "
             "is mainly used to compute work center costs during operations and to plan future loads on "
             "work centers based on production planning.")

    routing_id = fields.Many2one(
        'mrp.routing', 'Routing',
        readonly=False, compute='_compute_routing', store=True,
        help="The list of operations (list of work centers) to produce the finished product. The routing "
             "is mainly used to compute work center costs during operations and to plan future loads on "
             "work centers based on production planning.")
    tempreature = fields.Char('Tempreature')
    customer = fields.Many2one('res.partner','Customer')

    
    @api.multi
    @api.depends('routing_id2')
    def _compute_routing(self):
        for production in self:
            production.routing_id = production.routing_id2
            # if production.bom_id.routing_id.operation_ids:
            #     production.routing_id = production.bom_id.routing_id.id
            # else:
            #     print("DLLLLLLLLLLLLLLLL")
            #     # production.routing_id = False


    def _workorders_create(self, bom, bom_data):
        """
        :param bom: in case of recursive boms: we could create work orders for child
                    BoMs
        """
        workorders = self.env['mrp.workorder']
        bom_qty = bom_data['qty']

        # Initial qty producing
        if self.product_id.tracking == 'serial':
            quantity = 1.0
        else:
            quantity = self.product_qty - sum(self.move_finished_ids.mapped('quantity_done'))
            quantity = quantity if (quantity > 0) else 0

        for operation in self.routing_id.operation_ids:
            # create workorder
            cycle_number = float_round(bom_qty / operation.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
            duration_expected = (operation.workcenter_id.time_start +
                                 operation.workcenter_id.time_stop +
                                 cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)
            routing = self.routing_id
            temp = self.tempreature
            customer = self.customer
            workorder = workorders.create({
                'name': operation.name,
                'production_id': self.id,
                'workcenter_id': operation.workcenter_id.id,
                'operation_id': operation.id,
                'duration_expected': duration_expected,
                'state': len(workorders) == 0 and 'ready' or 'pending',
                'qty_producing': quantity,
                'capacity': operation.workcenter_id.capacity,
                'routing_id': routing.id,
                'tempreature': temp,
                'customer': customer.id,
            })
            print(workorder)
            if workorders:
                workorders[-1].next_work_order_id = workorder.id
                workorders[-1]._start_nextworkorder()
            workorders += workorder

            # assign moves; last operation receive all unassigned moves (which case ?)
            moves_raw = self.move_raw_ids.filtered(lambda move: move.operation_id == operation)
            if len(workorders) == len(bom.routing_id.operation_ids):
                moves_raw |= self.move_raw_ids.filtered(lambda move: not move.operation_id)
            moves_finished = self.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
            moves_raw.mapped('move_line_ids').write({'workorder_id': workorder.id})
            (moves_finished + moves_raw).write({'workorder_id': workorder.id})

            workorder._generate_lot_ids()
        return workorders


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    routing_id = fields.Many2one(
        'mrp.routing', 'Routing',
        readonly=False,
        help="The list of operations (list of work centers) to produce the finished product. The routing "
             "is mainly used to compute work center costs during operations and to plan future loads on "
             "work centers based on production planning.")

    tempreature = fields.Char('Tempreature')
    customer = fields.Many2one('res.partner', 'Customer')



class StockPicking(models.Model):
    _inherit='stock.picking'
    bom_line_ids = fields.One2many(comodel_name="picking.bom.line", inverse_name="pick_id", string="Lines", required=False)




class BomLines(models.Model):
    _name='picking.bom.line'

    pick_id = fields.Many2one(comodel_name="stock.picking")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", readonly=True)
    qty = fields.Float(string="Quantity", required=False)


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _run_pull(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        if not self.location_src_id:
            msg = _('No source location defined on stock rule: %s!') % (self.name,)
            raise UserError(msg)

        # create the move as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
        # Search if picking with move for it exists already:
        group_id = False
        if self.group_propagation_option == 'propagate':
            group_id = values.get('group_id', False) and values['group_id'].id
        elif self.group_propagation_option == 'fixed':
            group_id = self.group_id.id

        data = self._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values,
                                           group_id)
        # Since action_confirm launch following procurement_group we should activate it.
        move = self.env['stock.move'].sudo().with_context(force_company=data.get('company_id', False)).create(data)
        move._action_confirm()

        # get bom lines
        lines2=[]
        bom=self.env['mrp.bom'].search([('product_tmpl_id','=',product_id.product_tmpl_id.id)],limit=1)
        for line in bom.bom_line_ids:
            lines2.append((0, 0,
                          {'product_id': line.product_id.id,
                           'qty': line.product_qty,
                           'pick_id': move.picking_id.id,}
                          ))
        move.picking_id.write({'bom_line_ids':lines2})

        return True




