import base64
import xlrd
from odoo import models, fields


class ImportSaleOrderWizard(models.TransientModel):
    _name = 'import.sale.order.wizard'
    _description = 'Import Sale Order Wizard'

    filename = fields.Char(string="Filename")
    excel_file = fields.Binary(string='Excel File', required=True)

    def import_sale_orders(self):
        decoded_data = base64.decodebytes(self.excel_file)
        workbook = xlrd.open_workbook(file_contents=decoded_data)
        sheet = workbook.sheet_by_index(0)
        previous_sale_order_name = None
        order_no_val = {}
        for row in range(1, sheet.nrows):
            previous_sale_order_name = sale_order_name = sheet.cell_value(row, 0) or previous_sale_order_name
            partner_name = sheet.cell_value(row, 2)
            sale_person_name = sheet.cell_value(row, 3)
            company_name = sheet.cell_value(row, 4)
            partner = self.env['res.partner'].search([('name', '=', partner_name)], limit=1)
            sale_person = self.env['res.users'].search([('name', '=', sale_person_name)], limit=1)
            company = self.env['res.company'].search([('name', '=', company_name)], limit=1)
            product_name = sheet.cell_value(row, 6)
            product_id = self.env['product.template'].search([('name', '=', product_name)], limit=1)
            name = sheet.cell_value(row, 7)
            product_uom_qty = sheet.cell_value(row, 8)
            price_unit = sheet.cell_value(row, 9)
            tax_id = sheet.cell_value(row, 10)
            sale_order = None
            order_line_data = None
            if sale_order_name and partner:
                sale_order = {
                    # 'name': sale_order_name,
                    'partner_id': partner.id if partner else False,
                    'user_id': sale_person.id if sale_person else False,
                    'company_id': company.id if company else False,}
            if product_id:
                order_line_data = {
                    # 'product_template_id': product_id.id,
                    'product_id':product_id.product_variant_id.id,
                    'name': name,
                    'display_type':False,
                    'product_uom_qty': product_uom_qty,
                    'product_uom':product_id.uom_id.id,
                    'price_unit': price_unit,
                    'customer_lead':2.0,
                    'tax_id': False, }

            if sale_order_name not in order_no_val:
                order_no_val[sale_order_name] = [sale_order]
                if order_line_data:
                    order_no_val[sale_order_name].append([order_line_data])
            else:
                order_no_val[sale_order_name][1].append(order_line_data)

        for oder_no,  data in order_no_val.items():
            vals = data[0]
            line_list = []
            for line_data in data[1]:
                line_list.append((0, 0, line_data))
            vals['order_line'] = line_list
            self.env['sale.order'].create(vals)
