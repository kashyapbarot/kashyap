# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):
    """Purchase Order Inherit """
    _inherit = 'product.product'

    date_deadline = fields.Date(string='Deadline', index=True, copy=False)
    date_start = fields.Date(string='Start date', index=True, copy=False)



