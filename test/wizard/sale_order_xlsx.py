# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""

import xlrd
import logging
import tempfile
import binascii
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'sale.xlsx.wizard'
    _description = 'custom sale order wizard'

    file = fields.Binary(
        string='import Sale orders',
        required=True)

    def import_journal_sale_entry(self):
        if not self.file:
            raise ValidationError(_("Please Upload File to Import Employee !"))
        else:
            try:
                file = tempfile.NamedTemporaryFile(delete=False,
                                                   suffix=".xlsx")
                file.write(binascii.a2b_base64(self.file))
                file.seek(0)
                values = {}
                workbook = xlrd.open_workbook(file.name)
                sheet = workbook.sheet_by_index(0)
            except Exception:
                raise ValidationError(_("Please Select Valid File Format !"))

            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = list(map(lambda row: row.value.encode('utf-8'),
                                      sheet.row(row_no)))
                else:
                    line = list(map(lambda row: isinstance(row.value,
                                                           bytes) and row.value.encode(
                        'utf-8') or str(row.value), sheet.row(row_no)))
                    print("line", line)
                    values.update({
                        'Order Reference': line[0],
                        'Customer': line[1],
                        'Pricelist': line[2],
                        'Product': line[3],

                    })
                    res = self.create_sale_journal_entry(values)

    def create_sale_journal_entry(self, values):
        sale_order = self.env['sale.order']
        partner_name = values.get('Customer')
        sale_order_product = values.get('Product')

        product = self.env['product.product'].search(
            [('name', '=', sale_order_product)],
            limit=1)
        partner = self.env['res.partner'].search(
            [('name', '=', partner_name)],
            limit=1)
        print(partner)
        if not partner:
            self.env['res.partner'].create({
                'name': values.get('Customer'), })
        vals = {
            'name': values.get('Order Reference'),
            'partner_id': partner.id,
            'pricelist_id': self.env.ref("product.list0").id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 192,
                'discount': 74.246,
            })]
        }
        res = sale_order.create(vals)
        return res
