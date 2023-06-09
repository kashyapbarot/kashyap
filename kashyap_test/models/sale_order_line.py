# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


class SaleOrderLineInherit(models.Model):
    """add m2m field in sale order line"""
    _inherit = 'sale.order.line'

    tags_ids = fields.Many2many(
        comodel_name='doc.tag.master',
        string='Tags_ids')


class SaleOrderLine(models.Model):
    """add m2m field in product"""
    _inherit = 'product.template'

    documents_ids = fields.Many2many(comodel_name='documents.custom',
                                     string='Documents IDs')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        """"only product will be visible which are configure from customer public pricelist"""
        context = self._context or {}
        pricelist_select = context.get('pricelist')
        if pricelist_select:
            pricelist_table = self.env['product.pricelist'].browse(
                pricelist_select).item_ids.mapped('product_tmpl_id').ids
            print(args)
            args = expression.AND([[('id', 'in', pricelist_table)], args])
            print(args)
        return super()._search(args, offset=offset, limit=limit,
                               order=order,
                               count=count,
                               access_rights_uid=access_rights_uid)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     context = self._context or {}
    #     pricelist_select = context.get('pricelist')
    #     print(pricelist_select)
    #     if pricelist_select:
    #         pricelist_table = self.env['product.pricelist'].browse(
    #             pricelist_select).item_ids.mapped('product_tmpl_id').ids
    #         print(pricelist_table)
    #         print("args----------------", args)
    #         args = expression.AND([[('id', 'in', pricelist_table)], args])
    #     print("args111----------------", args)
    #     var = super()._name_search(name, args, operator, limit, name_get_uid)
    #     print(var)
    #     return var
