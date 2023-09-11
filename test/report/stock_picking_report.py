# -*- coding: utf-8 -*-
from pdf2image import convert_from_bytes

from odoo import models, fields, api


class StockPickingReport(models.Model):
    _inherit = "stock.picking"

    # @api.onchange('stock_attachment_ids')
    # def _pdf_to_image(self):
    #     images = convert_from_bytes('Document.pdf',
    #         poppler_path=r"poppler-0.68.0_x86\poppler-0.68.0\bin")
    #     for i in range(len(images)):
    #         # Save pages as images in the pdf
    #         images[i].save(f'image_{i + 1}.png', 'PNG')
    #     print("yes")
    #     self.stock_attachment_ids = images


# class IrAttachment(models.Model):
#     _inherit = "ir.attachment"
