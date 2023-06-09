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
    # download_file_data = fields.Binary(string="Download", related='attachment_id.datas')
    tag_ids = fields.Many2many(comodel_name='doc.tag.master', string='Tags')


class DocTagMaster(models.Model):
    _name = 'doc.tag.master'
    _description = 'Doc Tag Master'

    name = fields.Char(string="Name")


class CustomerMaster(models.Model):
    """add field in res partner"""
    _inherit = 'res.partner'

    customer_tag_ids = fields.Many2many(comodel_name='doc.tag.master',
                                        string='Tags')


class SaleOrder(models.Model):
    """add field in sale order"""
    _inherit = 'sale.order'

    tags_ids = fields.Many2many(comodel_name='doc.tag.master', string='Tags')
    documents_ids = fields.Many2many(comodel_name='documents.custom',
                                     string='Documents')

    @api.onchange('partner_id')
    def validate_customer(self):
        """for store values"""
        for rec in self:
            if rec.partner_id:
                rec.tags_ids = rec.partner_id.customer_tag_ids
            else:
                rec.tags_ids = None

    def get_documents(self):
        doc_ids = []
        tag_ids = self.tags_ids.ids
        product_doc_ids = self.mapped(
            "order_line.product_template_id.documents_ids")
        for rec in product_doc_ids:
            for i in rec.tag_ids:
                if i.id in tag_ids:
                    self.documents_ids = doc_ids.append(rec.id)

        # def get_documents(self):
        #     doc_ids = []
        #     tag_ids = self.tags_ids.ids
        #     product_doc_ids = self.order_line.mapped(
        #         'product_template_id.documents_ids')
        #     for rec in product_doc_ids:
        #         for rt in rec.tag_ids:
        #             if rt.id in tag_ids and rec.id not in doc_ids:
        #                 doc_ids.append(rec.id)
        #     self.documents_ids = [(6, 0, doc_ids)]

        # for rec in self:
        #     rec.documents_ids = [(5, 0, 0)]
        #
        # def compare_lists(list1, list2):
        #     matched_elements = [element for element in list1 if
        #                         element in list2]
        #     return matched_elements[0] if matched_elements else None
        #
        # if self.partner_id and self.tags_ids:
        #     tags = self.mapped('tags_ids').ids
        #     documents = self.mapped(
        #         'order_line.product_template_id.documents_ids')
        #     document_list = []
        #     for x in documents:
        #         doc = x.mapped('tag_ids').ids
        #         if compare_lists(doc, tags):
        #             document_list.append(x.id)
        #     self.documents_ids = document_list

        # tags = self.mapped('tags_ids').ids
        # documents = self.mapped('order_line.product_template_id.documents_ids')
        # self.documents_ids = [doc.id for doc in documents if
        #                       any(compare_lists(doc.mapped('tag_ids').ids,
        #                                         tags))]

        # def get_documents(self):
        #     tag_ids = self.tags_ids.ids
        #     doc_ids = [rec.id for rec in self.order_line.mapped(
        #         'product_template_id.documents_ids')
        #                if any(rt.id in tag_ids for rt in rec.tag_ids)]
        #     self.documents_ids = [(6, 0, doc_ids)] if doc_ids else []