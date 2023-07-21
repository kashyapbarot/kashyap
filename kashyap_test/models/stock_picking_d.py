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


class StockMove(models.Model):
    """add field on delivery order"""
    _inherit = 'stock.move'

    unit_price_new = fields.Float(
        string='Unit Price', readonly=True)

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        # var = self.group_id.sale_id.data
        # name_str = self.group_id.sale_id.name
        # print(var, name_str)
        res.update({'s_data': self.group_id.sale_id.data})
        # self.env.cr.execute("""INSERT INTO stock_picking(s_data) VALUES('rahul')""")

        # self.env.cr.execute("""UPDATE stock_picking SET s_data= '%s' WHERE origin = '%s'""" % (self.group_id.sale_id.data, self.group_id.sale_id.name))
        # self.env.cr.execute("""SELECT *from stock_picking WHERE origin = %s"""%(name_str))
        # var1=self.env.cr.fetchall()
        # print(var1)
        return res
