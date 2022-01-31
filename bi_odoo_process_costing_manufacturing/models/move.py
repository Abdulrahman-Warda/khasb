from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
        self.ensure_one()
        AccountMove = self.env['account.move']
        quantity = self.env.context.get('forced_quantity', self.product_qty)
        quantity = quantity if self._is_in() else -1 * quantity
        ref = self.picking_id.name
        if self.env.context.get('force_valuation_amount'):
            if self.env.context.get('forced_quantity') == 0:
                ref = 'Revaluation of %s (negative inventory)' % ref
            elif self.env.context.get('forced_quantity') is not None:
                ref = 'Correction of %s (modification of past move)' % ref
        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(quantity, abs(self.value),
                                                                                  credit_account_id, debit_account_id)
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))

            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })
            print("new_account_move", new_account_move)
            new_account_move.post()
        if self.production_id:
            # self.create_labour_move(journal_id,date,ref,self.production_id)
            # self.create_material_move(journal_id,date,ref,self.production_id)
            self.create_overhead_move(journal_id, date, ref, self.production_id)

    def create_labour_move(self, journal_id, date, ref, production_id):
        move_lines = []
        # if self.production_id
        AccountMove = self.env['account.move']
        sum = 0
        for line in production_id.pro_labour_cost_ids:
            sum += line.total_actual_cost
            debit_line_vals = {
                'name': self.name,
                'ref': ref,
                'debit': line.total_actual_cost,
                'credit': 0,
                'account_id': line.debit_account_id.id,
            }
            credit_line_vals = {
                'name': self.name,
                'ref': ref,
                'credit': line.total_actual_cost,
                'debit': 0,
                'account_id': line.credit_account_id.id,
            }
            move_lines.append((0, 0, debit_line_vals))
            move_lines.append((0, 0, credit_line_vals))
        if sum > 0:
            AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })

    def create_material_move(self, journal_id, date, ref, production_id):
        move_lines = []
        # if self.production_id
        AccountMove = self.env['account.move']
        sum = 0
        for line in production_id.pro_material_cost_ids:
            sum += line.total_actual_cost
            debit_line_vals = {
                'name': self.name,
                'ref': ref,
                'debit': line.total_actual_cost,
                'credit': 0,
                'account_id': line.debit_account_id.id,
            }
            credit_line_vals = {
                'name': self.name,
                'ref': ref,
                'credit': line.total_actual_cost,
                'debit': 0,
                'account_id': line.credit_account_id.id,
            }
            move_lines.append((0, 0, debit_line_vals))
            move_lines.append((0, 0, credit_line_vals))

        if sum > 0:
            AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })

    def create_overhead_move(self, journal_id, date, ref, production_id):
        move_lines = []
        # if self.production_id
        sum = 0
        AccountMove = self.env['account.move']
        for line in production_id.pro_overhead_cost_ids:
            sum += line.total_actual_cost
            debit_line_vals = {
                'name': self.name,
                'ref': ref,
                'debit': line.total_actual_cost,
                'credit': 0,
                'account_id': line.debit_account_id.id,
            }
            credit_line_vals = {
                'name': self.name,
                'ref': ref,
                'credit': line.total_actual_cost,
                'debit': 0,
                'account_id': line.credit_account_id.id,
            }
            move_lines.append((0, 0, debit_line_vals))
            move_lines.append((0, 0, credit_line_vals))
        if sum:
            AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })
