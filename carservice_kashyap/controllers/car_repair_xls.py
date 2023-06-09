# # -*- coding: utf-8 -*-
import io
import xlwt
from odoo import http, _
from odoo.http import request


class ExportPurchaseExcel(http.Controller):
    @http.route('/carservice_kashyap/export_excel', type='http',
                auth="user")
    def export_excel(self, **kwargs):
        # get the report ID from the request parameters
        report_id = int(kwargs.get('target_report'))

        # search for the purchase order with the given ID
        po = request.env['car.repair.order.wizard'].search(
            [('id', '=', report_id)])
        start_date = po.s_date
        end_date = po.e_date

        po = request.env['car.repair.order'].search(
            [('date', '>=', start_date), ('date', '<=', end_date)])
        # po_ids = po.t_ids
        # create a new Excel workbook and worksheet
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('CarRepair', cell_overwrite_ok=True)

        # # define a style for the headers
        style0 = xlwt.easyxf(
            'font: name Times New Roman, color-index red, bold on',
            num_format_str='#,##0.00')
        style1 = xlwt.easyxf('align: horiz center')

        worksheet.col(0).width = 7000
        worksheet.col(1).width = 7000
        worksheet.col(2).width = 7000
        worksheet.col(3).width = 7000
        worksheet.col(4).width = 7000
        worksheet.col(5).width = 7000

        worksheet.write(0, 0, 'From Date', style0)
        worksheet.write(0, 1, str(start_date), style1)
        worksheet.write(1, 0, 'To Date', style0)
        worksheet.write(1, 1, str(end_date), style1)

        worksheet.write(2, 0, 'technician', style0)
        worksheet.write(2, 1, 'Total Repair Order', style0)
        row = 0
        for row, data in enumerate(po):
            column = 0
            worksheet.write(row + 3, column, data.technician_id.name)
            column += 1
            worksheet.write(row + 3, column,
                            request.env['car.repair.order'].search_count([(
                                'technician_id',
                                '=',
                                data.technician_id.id)]))
            worksheet.write(row + 2, 3, 'Total', style1)
            worksheet.write(row + 2, 4, sum(
                list.total_order for list in po))

        report_name = 'po.xls'
        # create a response with the Excel file as the content
        response = request.make_response(None,
                                         headers=[
                                             ('Content-Type',
                                              'application/vnd.ms-excel'),
                                             ('Content-Disposition',
                                              'attachment; filename=' + report_name)])

        workbook.save(response.stream)
        return response
