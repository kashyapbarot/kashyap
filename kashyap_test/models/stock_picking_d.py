# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.picking'

    documents_delivery_ids = fields.Many2many(comodel_name='documents.custom',
                                              string='Documents Delivery')


class StockMove(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.move'

    unit_price_new = fields.Float(
        string='Unit Price', readonly=True)
