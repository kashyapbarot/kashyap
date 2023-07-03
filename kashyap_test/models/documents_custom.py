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


class CustomerMaster(models.Model):
    """add field in res partner"""
    _inherit = 'res.partner'

    customer_tag_ids = fields.Many2many(comodel_name='doc.tag.master',
                                        string='Tags')


class CrmLead(models.Model):
    _inherit = 'crm.lead'


class SaleOrder(models.Model):
    """add field in sale order"""
    _inherit = 'sale.order'

    data = fields.Char(
        string='Data',
        required=False)
    tags_ids = fields.Many2many(comodel_name='doc.tag.master', string='Tags')
    documents_ids = fields.Many2many(comodel_name='documents.custom',
                                     string='Documents')
    campaign_new_id = fields.Many2one(comodel_name='utm.campaign',
                                      string='Campaign',
                                      required=False, readonly=True,
                                      related='campaign_id')
    medium_new_id = fields.Many2one(comodel_name='utm.medium',
                                    string='Medium',
                                    required=False, readonly=True,
                                    related='medium_id')
    source_new_id = fields.Many2one(comodel_name='utm.source',
                                    string='Source',
                                    required=False, readonly=True,
                                    related='source_id')
    sale_order_count = fields.Integer(compute='compute_count', string="")

    def get_sales(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale',
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'domain': [('partner_id', 'in', self.partner_id.ids)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        for record in self:
            record.sale_order_count = self.env['sale.order'].search_count(
                [('partner_id', 'in', self.partner_id.ids)])

    # @api.onchange('partner_id')
    # def validate_customer(self):
    #     """for store values"""
    #     for rec in self:
    #         if rec.partner_id:
    #             rec.tags_ids = rec.partner_id.customer_tag_ids
    #         else:
    #             rec.tags_ids = None

    def refresh_field(self):
        if self.tags_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def action_confirm(self):
        """"create record in Stock Move"""
        res = super().action_confirm()
        for rec in self.order_line:
            rec.move_ids.write({'unit_price_new': rec.price_unit})
        # self.picking_ids.s_data = self.data
        return res

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

    def write(self, vals):
        """"create record in Stock Move"""
        res = super().write(vals)
        for rec in self.order_line:
            rec.move_ids.write({'unit_price_new': rec.price_unit})
        return res

        # def action_confirm(self):
        #     """"create record in OD"""
        #     res = super().action_confirm()
        #     self.picking_ids.documents_delivery_ids = [
        #         (6, 0, self.mapped('documents_ids').ids)]
        #     return res

        # for rec in self:
        #     rec.documents_ids = [(5, 0, 0)]
        #
        # def compare_lists(list1, list2):
        #     matched_elements = [element for element in list1 if
        #                         element in list2]
        #     return matched_elements[0] if matched_elements else None

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

    # def create(self, vals):
    #     self.picking_ids.s_data = (0, 0, self.data)
    #     res = super().create(vals)
    #     print("11111----", vals)
    #     return res
