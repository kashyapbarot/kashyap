# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""

from datetime import datetime, timedelta
from odoo import models, fields, api, _
import xlrd

from odoo.exceptions import UserError


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'sale.xlsx.wizard'
    _description = 'custom sale order wizard'

    sale = fields.Binary(
        string='import Sale orders',
        required=True)

    def import_journal_sale_entry(self):
        try:
            book = xlrd.open_workbook(filename=self.sale)
            print(book)
        except FileNotFoundError:
            raise UserError(
                'No such file or directory found. \n%s.' % self.sale)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            try:
                line_vals = []
                if sheet.name == 'Sheet1':
                    for row in range(sheet.nrows):
                        if row >= 1:
                            row_values = sheet.row_values(row)
                            vals = self._create_sale_journal_entry(row_values)
                            line_vals.append((0, 0, vals))
                if line_vals:
                    self.env['sale.order'].create({
                        'line_ids': line_vals
                    })
            except IndexError:
                pass

    def _create_sale_journal_entry(self, record):
        line_ids = {
            'activity_ids': record[0],
            'company_id': record[1],
            'create_date': record[2],
            'partner_id': record[3],
            'commitment_date': record[4],
            'expected_date': record[5],
            'invoice_status': record[6],
            'name': record[7],
            'team_id': record[8],
            'user_id': record[9],
            'state': record[10],
            'tag_ids': record[11],
            'amount_tax': record[12],
            'amount_total': record[13],
            'amount_untaxed': record[14],
            'order_line': record[15],
        }
        return line_ids
