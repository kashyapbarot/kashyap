import xlrd
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'sale.xlsx.wizard'
    _description = 'custom sale order wizard'

    file = fields.Binary(
        string='import Sale orders',
        required=True)

    def import_journal_entry(self):
        try:
            book = xlrd.open_workbook(filename=self.file)
        except FileNotFoundError:
            raise UserError(
                'No such file or directory found. \n%s.' % self.file)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            try:
                line_vals = []
                if sheet.name == 'Sheet1':
                    for row in range(sheet.nrows):
                        if row >= 1:
                            row_values = sheet.row_values(row)
                            vals = self._create_journal_entry(row_values)
                            line_vals.append((0, 0, vals))
                if line_vals:
                    date = self.date
                    ref = self.jv_ref
                    self.env['account.move'].create({
                        'date': date,
                        'ref': ref,
                        'journal_id': self.jv_journal_id.id,
                        'line_ids': line_vals
                    })
            except IndexError:
                pass

    def _create_journal_entry(self, record):
        code = int(record[0])
        account_id = self.env['account.account'].search([('code', '=', code)],
                                                        limit=1)
        if not account_id:
            raise UserError(_("There is no account with code %s.") % code)
        partner_id = self.env['res.partner'].search([('name', '=', record[2])],
                                                    limit=1)
        if not partner_id:
            partner_id = self.env['res.partner'].create({
                'name': record[1],
                'customer': True,
            })
        line_ids = {
            'account_id': account_id.id,
            'partner_id': partner_id.id,
            'name': record[1],
            'debit': record[4],
            'credit': record[5],
        }
        return line_ids
