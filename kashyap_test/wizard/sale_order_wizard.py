# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""

from odoo import models, fields


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'custom.sale.order'
    _description = 'custom sale order wizard'

    def _default_get_record(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    t_ids = fields.Many2many(
        comodel_name='sale.order',
        string='Record', default=_default_get_record)

    def generate_report(self):
        url = '/kashyap_test/export_excel?target_report=%s' % self.id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
            'context': {'active_ids': self._default_get_record}
        }
