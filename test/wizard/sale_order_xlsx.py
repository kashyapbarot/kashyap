# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""
import base64

import xlrd
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'sale.xlsx.wizard'
    _description = 'custom sale order wizard'

    file_name = fields.Char('File Name')
    file = fields.Binary(
        string='import Sale orders',
        required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=False)

    def import_journal_sale_entry(self):
        try:
            decoded_data = base64.decodebytes(self.file)
            book = xlrd.open_workbook(file_contents=decoded_data)
        except FileNotFoundError:
            raise UserError(
                'No such file or directory found. \n%s.' % self.file)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            try:
                sale_line_vals = []
                if sheet.name == 'Sheet1':
                    for row in range(sheet.nrows):
                        if row >= 1:
                            row_values = sheet.row_values(row)
                            vals = self.create_sale_journal_entry(row_values)
                            sale_line_vals.append((0, 0, vals))
                if sale_line_vals:
                    partner = self.partner_id
                    self.env['sale.order'].create({
                        'partner_id': partner.id,
                        'pricelist_id': self.env.ref("product.list0").id,
                        'order_line': sale_line_vals
                    })
            except IndexError:
                pass

    def create_sale_journal_entry(self, record):
        code = record[0]
        print("code")
        product_id = self.env['product.product'].search([('code', '=', code)],
                                                        limit=1)
        if not product_id:
            raise UserError(_("There is no product with code %s.") % code)

        order_line = {
            'product_id': product_id.id,
            'name': record[1],
            'product_uom_qty': record[2],
            'price_unit': record[3],
        }
        return order_line
