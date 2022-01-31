# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class SplitManufacturing(models.TransientModel):	
	_name = "split.mo.order"
	_description = "Split Manufacturing"

	spliting_method = fields.Selection([('by_qty', 'By Number of Quantity'), ('by_split', 'By Number of Split')],string = 'Spliting Method', required=True)
	no_qty = fields.Integer("Number of Quantity")
	no_split = fields.Integer("Number of Split")

	# split Manufacturing using number of qty and number of split mo
	def split_confirm(self):
		current_id = self._context.get('active_id')
		mo_order = self.env['mrp.production'].browse(current_id)

		if self.spliting_method == 'by_split':
			if self.no_split <= 0:
				raise Warning(_('Please enter data for split number of Manufacturing Orders..!')) 

			divide_qty = mo_order.product_qty/self.no_split
			mo_order.write({'product_qty':divide_qty})
			no_split = self.no_split-1

			for i in range(0,no_split):
				new_mo_order = self.env['mrp.production'].create({
										'product_id':mo_order.product_id.id,
										'product_qty':divide_qty,
										'bom_id':mo_order.bom_id.id,
										'date_planned_start':mo_order.date_planned_start,
										'date_planned_finished':mo_order.date_planned_finished,
										'product_uom_id':mo_order.product_uom_id.id,
										})

				new_mo_order.action_assign()

			for line in mo_order.move_raw_ids:
				line.write({'product_uom_qty':line.product_uom_qty/self.no_split})

		if self.spliting_method == 'by_qty':
			if self.no_qty <= 0:
				raise Warning(_('Please enter valid Number of Quantity...!'))
			if self.no_qty > mo_order.product_qty:
				raise Warning(_('Please enter smaller qty than current MO Qty...!'))

			new_mo = self.env['mrp.production'].create({
									'product_id':mo_order.product_id.id,
									'product_qty':self.no_qty,
									'bom_id':mo_order.bom_id.id,
									'date_planned_start':mo_order.date_planned_start,
									'date_planned_finished':mo_order.date_planned_finished,
									'product_uom_id':mo_order.product_uom_id.id,
									})

			new_mo.action_assign()

			for line in mo_order.move_raw_ids:
				div_qty = line.product_uom_qty/mo_order.product_qty
				final_line_qty = (div_qty * self.no_qty)
				line.write({'product_uom_qty':line.product_uom_qty-final_line_qty})
			mo_order.write({'product_qty':mo_order.product_qty - self.no_qty})
