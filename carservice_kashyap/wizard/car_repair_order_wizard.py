# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""

from odoo import models, fields


class CarRepairWizard(models.TransientModel):
    """Vendor Wizard Class"""
    _name = 'car.repair.order.wizard'
    _description = 'Car Repair Order Wizard'

    s_date = fields.Date(string='Start Date', required=False)
    e_date = fields.Date(string='End Date', required=False)
    t_ids = fields.Many2many(
        comodel_name='car.repair.order',
        string='Technician')
    # total_order = fields.Integer(
    #     string='Total Repair order',
    #     required=False)

    def generate_report(self):
        url = '/carservice_kashyap/export_excel?target_report=%s' % self.id

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }