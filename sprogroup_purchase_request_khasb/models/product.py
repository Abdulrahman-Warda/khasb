from odoo import api, fields, models

class Product_Template(models.Model):
    _inherit = 'product.category'

    internal_product = fields.Boolean('Internal Products')
    private_product = fields.Boolean('Manufacturing Products')
