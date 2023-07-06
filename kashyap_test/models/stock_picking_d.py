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

    # def _assign_picking(self):
    #     self.create({'s_data': self.group_id.sale_id.data})
    #     print("-----------------------------------")
    #     return super()._assign_picking()


class StockMove(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.move'

    unit_price_new = fields.Float(
        string='Unit Price', readonly=True)

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        res.update({'s_data': self.group_id.sale_id.data})
        return res
