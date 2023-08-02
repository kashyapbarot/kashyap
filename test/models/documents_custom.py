# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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


class SaleOrderLineInherit(models.Model):
    """add m2m field in sale order line"""
    _inherit = 'sale.order.line'

    tags_ids = fields.Many2many('doc.tag.master', string='Tags_ids')
    bom_new_id = fields.Many2one('mrp.bom', string='Bom')

    is_mto_and_m = fields.Boolean(string="MTO&M", default=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def check_invantory_in_mto_and_m(self):
        for order in self.order_line:
            var = order.product_template_id.route_ids.ids
            mto_and_m_id = [self.env.ref('stock.route_warehouse0_mto').id,
                            self.env.ref(
                                'mrp.route_warehouse0_manufacture').id]
            if var == mto_and_m_id:
                order.is_mto_and_m = True
            else:
                order.is_mto_and_m = False

    def action_sale_order(self):
        count_record = self.search([('state', '=', 'draft')])
        for rec in count_record:
            rec.state = 'sent'
            # mail_template_id = self.env.ref("sale.email_template_edi_sale").id
            # email_template = self.env['mail.template'].browse(mail_template_id)
            # email_template.send_mail(rec.id, force_send=True)
            mail_template = self.env.ref("sale.email_template_edi_sale")
            if mail_template:
                vals = {
                    'model': 'sale.order',
                    'res_id': rec.id,
                    'template_id': mail_template.id if mail_template else None,
                    'composition_mode': 'comment',
                }
                p = self.env['mail.compose.message'].with_context(
                    default_use_template=bool(mail_template),
                    mark_so_as_sent=True,
                    proforma=self.env.context.get('proforma', False),
                    force_email=True, mail_notify_author=True
                ).create(vals)
                update_values = \
                    p._onchange_template_id(mail_template.id, 'comment',
                                            'sale.order',
                                            rec.id)[
                        'value']
                p.write(update_values)

                p._action_send_mail()


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom,
                         location_dest_id, name, origin, company_id, values,
                         bom):
        # values.get('group_id').sale_id.order_line.bom_new_id
        # bom_new_id = values.get('move_dest_ids').sale_line_id.bom_new_id
        # res.update({'bom_id': bom_new_id.id})
        return super()._prepare_mo_vals(product_id, product_qty,
                                        product_uom,
                                        location_dest_id, name, origin,
                                        company_id, values,
                                        bom=values.get(
                                            'move_dest_ids').sale_line_id.bom_new_id or bom)
