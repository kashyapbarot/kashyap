# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DocumentsCustom(models.Model):
    """" For documents custom module"""
    _name = 'documents.custom'
    _description = 'Documents Custom'

    name = fields.Char(string="Name")
    attachment_id = fields.Many2one(comodel_name='ir.attachment',
                                    string='Attachment id',
                                    required=False)
    download_file_data = fields.Binary(string="Download",
                                       related='attachment_id.datas')
    tag_ids = fields.Many2many(comodel_name='doc.tag.master', string='Tags')
    m_count = fields.Integer(compute="compute_m2m")


class DocTagMaster(models.Model):
    _name = 'doc.tag.master'
    _description = 'Doc Tag Master'

    name = fields.Char(string="Name")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create_product_record(self, vals_list):
        """"create product and BOM using external api"""
        product_1 = self.create(vals_list.get('product_1'))
        product_2 = self.create(vals_list.get('product_2'))
        # Create BOM of product_2 with product_1 as component
        product_2.bom_ids.create(
            {'product_tmpl_id': product_2.id, "product_qty": 200,
             'product_id': product_2.product_variant_id.id,
             'bom_line_ids': [
                 (0, 0, {'product_qty': 1,
                         'product_id': product_1.product_variant_id.id,
                         'product_tmpl_id': product_1.id})]})
        return vals_list
