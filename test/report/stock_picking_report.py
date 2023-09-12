# -*- coding: utf-8 -*-
import base64
import io
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from odoo import models, fields, api


class StockPickingReport(models.Model):
    _inherit = "stock.picking"


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """" add PDF in  DO report"""
        result = super()._render_qweb_pdf(report_ref, res_ids=res_ids,
                                          data=data)
        report_ref_id = self.env.ref(
            'test.action_report_stock_picking')
        po_test_rep = 'test.report_stock_picking_shipment'
        report_ref_test = False
        if isinstance(report_ref, str) and report_ref == po_test_rep:
            report_ref_test = True
        elif not isinstance(report_ref,
                            str) and report_ref == report_ref_id:
            report_ref_test = True

        if res_ids and report_ref and report_ref_test:
            picking_id = self.env['stock.picking'].browse(res_ids)
            if picking_id:
                def append_pdf(input, output):
                    [output.addPage(input.getPage(page_num)) for page_num
                     in range(input.getNumPages())]

                output = PdfFileWriter()
                encoded_pdf = base64.b64encode(result[0])
                append_pdf(
                    PdfFileReader(io.BytesIO(base64.b64decode(encoded_pdf)),
                                  strict=False), output)
                for line in picking_id.stock_attachment_ids:
                    bin_file = line.datas
                    if bin_file:
                        pdf_content = base64.b64decode(bin_file)
                        pdf_reader = PyPDF2.PdfFileReader(
                            io.BytesIO(pdf_content))
                        append_pdf(pdf_reader, output)

                with open('/tmp/final.pdf', 'wb') as output_file:
                    output.write(output_file)

                with open('/tmp/final.pdf', 'rb') as output_file:
                    output_byte = output_file.read()
                    result = list(result)
                    result[0] = output_byte
                    result = tuple(result)
            return result
