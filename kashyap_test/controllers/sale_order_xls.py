# # -*- coding: utf-8 -*-
import io
import xlwt
from datetime import datetime
from odoo import http, _
from odoo.http import request


class ExportPurchaseExcel(http.Controller):
    @http.route('/kashyap_test/export_excel', type='http',
                auth="user")
    def export_excel(self, **kwargs):
        # get the report ID from the request parameters
        report_id = kwargs.get('target_report')
        # search for the purchase order with the given ID
        po = request.env['custom.sale.order'].search(
            [('id', '=', report_id)]).mapped('t_ids')
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('SaleOrder', cell_overwrite_ok=True)
        style1 = xlwt.easyxf('align: horiz center')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 7000
        worksheet.col(2).width = 10000
        worksheet.col(3).width = 10000
        worksheet.col(4).width = 10000
        worksheet.col(5).width = 7000
        worksheet.col(6).width = 7000
        worksheet.write(0, 0, 'Name', style1)
        worksheet.write(0, 1, 'Creation Date', style1)
        worksheet.write(0, 2, 'Customer', style1)
        worksheet.write(0, 3, 'Salesperson', style1)
        worksheet.write(0, 4, 'Company', style1)
        worksheet.write(0, 5, 'Total', style1)
        worksheet.write(0, 6, 'Status', style1)
        row = 0
        for row, data in enumerate(po):
            column = 0
            print(row)
            worksheet.write(row + 1, column, data.name, style1)
            column += 1
            worksheet.write(row + 1, column, str(datetime.date(data.create_date)), style1)
            column += 1
            worksheet.write(row + 1, column, data.partner_id.name, style1)
            column += 1
            worksheet.write(row + 1, column, data.user_id.name, style1)
            column += 1
            worksheet.write(row + 1, column, data.company_id.name, style1)
            column += 1
            worksheet.write(row + 1, column, f'${data.amount_total}', style1)
            column += 1
            worksheet.write(row + 1, column, data.state, style1)

        report_name = 'po.xls'
        response = request.make_response(None,
                                         headers=[
                                             ('Content-Type',
                                              'application/vnd.ms-excel'),
                                             ('Content-Disposition',
                                              'attachment; filename=' + report_name)])

        workbook.save(response.stream)
        return response
