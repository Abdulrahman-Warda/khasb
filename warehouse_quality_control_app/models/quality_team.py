# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class quality_team(models.Model):
    _name = "quality.team"

    name = fields.Char(string='Name')
    alias_id = fields.Many2one('mail.alias',string="Email Alias",ondelete="restrict")
    alias_name = fields.Char('Email Alias')


class quality_alert(models.Model):
    _name = "quality.alert"

    _inherit = ['mail.thread']

    name = fields.Char('name',readonly=True)
    title = fields.Char('Title')
    product_temp_id = fields.Many2one('product.template',string="Product")
    product_id = fields.Many2one('product.product',string="Product Variant")
    lot_id = fields.Many2one('stock.production.lot',string="LOT")

    user_id = fields.Many2one('res.users',string="Responsible")
    priority = fields.Selection([('n','normal'),('l','low'),('h','high'),('v','very_high')],string='Priority',default='n')

    description = fields.Html(string="description")
    correct_actions = fields.Html(string="Correct Actions")
    preventive_actions = fields.Html(string="Preventive Actions")
    partner_id = fields.Many2one('res.partner',string="Vendor")
    date_assigned = fields.Datetime(string="Date Assigned")
    date_close = fields.Datetime(string="Date Close")
    state_id = fields.Many2one('quality.alert.stage',string="State")
    tag_ids = fields.Many2many('quality.tags',string="Tags")
    picking_id = fields.Many2one('stock.picking',string="Picking")
    team_id = fields.Many2one('quality.team',string="Team")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('quality.alert') or '/'
        vals['name'] = seq
        if self._context.get('picking_res') :
            vals['picking_id'] = int(self._context.get('picking_res'))
        return super(quality_alert, self).create(vals)


class quality_alert_stage(models.Model):
    _name = "quality.alert.stage"

    name = fields.Char('Name')


class quality_tags(models.Model) :
    _name = "quality.tags"

    name = fields.Char('Name')