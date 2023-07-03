# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.picking'

    documents_delivery_ids = fields.Many2many(comodel_name='documents.custom',
                                              string='Documents Delivery')
    s_data = fields.Char(
        string='Data',
        required=False)

    def create(self, vals):
        id = vals.get('origin')
        vals['s_data'] = self.env['sale.order'].search([("name", '=', id)]).data
        res = super().create(vals)
        return res


class StockMove(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.move'

    unit_price_new = fields.Float(
        string='Unit Price', readonly=True)
