# -*- coding: utf-8 -*-
import base64
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

    # def refresh_field(self):
    #     att = self.attachment_id
    #     if att:
    #         res = self.env['ir.attachment'].browse(att.ids).datas
    #         return {
    #             "type": "ir.actions.act_url",
    #             "url": res,
    #             "target": "new", }


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

    def refresh_field(self):
        if self.tags_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def get_documents(self):
        """create record in documents page"""
        doc_ids = []
        tag_ids = self.tags_ids.ids
        product_doc_ids = self.order_line.mapped(
            'product_template_id.documents_ids')
        for rec in product_doc_ids:
            for rt in rec.tag_ids:
                if rt.id in tag_ids and rec.id not in doc_ids:
                    doc_ids.append(rec.id)
        self.documents_ids = [(6, 0, doc_ids)]

    def action_confirm(self):
        """"create record in OD"""
        res = super().action_confirm()
        self.picking_ids.documents_delivery_ids = [
            (6, 0, self.mapped('documents_ids').ids)]
        return res

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
