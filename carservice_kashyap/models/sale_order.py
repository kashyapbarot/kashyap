# -*- coding: utf-8 -*-
"""sale order"""

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # property_id = fields.Many2one(
    #     comodel_name='',
    #     string='Property',
    #     required=False)
