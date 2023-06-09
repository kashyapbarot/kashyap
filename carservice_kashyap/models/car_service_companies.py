# -*- coding: utf-8 -*-
"""Car Service Companies/workshops"""

from odoo import models, fields


class CarMaster(models.Model):
    """table structure car service companies"""
    _inherit = "fleet.vehicle"

    car_master = fields.Boolean(
        string='car',
        required=False)
