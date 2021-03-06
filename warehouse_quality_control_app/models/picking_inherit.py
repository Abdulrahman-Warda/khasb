# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class quality_point(models.Model):
    _inherit = "stock.picking"

    quality_checks = fields.Boolean(string="Quality Checks",compute="_compute_quality_check")

    @api.multi
    def button_validate(self):
        res = super(quality_point, self).button_validate()
        checks = self.env['quality.checks'].search([('picking_id','=',self.id),('state','=','do')])
        
        if checks :
            raise UserError(_(' You still need to do the quality checks!'))

        return res

    def _compute_quality_check(self):
        for line in self :

            for move in line.move_ids_without_package :

                quality_checks  = self.env['quality.checks'].search([('picking_id','=',line.id),('state','=','do')])
        
                if quality_checks :
                    line.quality_checks = True

                else :

                    line.quality_checks = False

        return

    def create_quality_alert(self):

        view_id = self.env.ref('warehouse_quality_control_app.view_quality_alert_form').id

        return {
            'name': 'Quality Checks',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {'picking_res':self.id},
            'res_model': 'quality.alert',
            'views': [(view_id,'form')],
        }

    def open_quality_alert(self):

        #view_id = self.env.ref('warehouse_quality_control_app.view_quality_alert_form').id

        action = self.env.ref('warehouse_quality_control_app.quality_alert_action_id').read()[0]
        action['domain'] = [('picking_id','=',self.id)]
        return action

    def action_check_wizard_picking(self):
        action = self.env.ref('warehouse_quality_control_app.action_check_wizard').read()[0]
        checks = self.env['quality.checks'].search([('picking_id','=',self.id),('state','=','do')],)
        for quality in checks :

            action['res_id'] = quality.id
            
            return action

    def action_open_checkes(self) :

        action = self.env.ref('warehouse_quality_control_app.qualitychecks_action_id').read()[0]
        action['domain'] = [('picking_id','=',self.id)]
        return action

class stockmove(models.Model):
    _inherit = "stock.move"

    def _action_assign(self):

        res = super(stockmove, self)._action_assign()
        for move in self :
            if move.picking_id :
                quality_checks = self.env['quality.point'].search([('picking_type_id','=',move.picking_id.picking_type_id.id),('product_id','=',move.product_id.id)],limit=1)
                if quality_checks :
                    self.env['quality.checks'].create({'product_id' : move.product_id.id,
                                                        'picking_id': move.picking_id.id,
                                                        'quality_point_id' : quality_checks.id,
                                                        'state':'do',
                                                        })

        return res