# -*- coding: utf-8 -*-
"""Car Service Companies/workshops"""
from odoo import models, fields, api


class RepairType(models.Model):
    """table structure Car Repair Type:"""
    _name = 'repair.type'
    _description = 'Repair Type'

    name = fields.Char(string='Name', required=True)
    service_type = fields.Selection(string='Service Type',
                                    selection=[('one', 'Long-term'),
                                               ('two', 'Short-Term'),
                                               ('three', 'Seasonal CHECK-UP'),
                                               ('four', 'Other')],
                                    required=False)
    active = fields.Boolean(string='Active', required=False)

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name must be unique !')
    ]
