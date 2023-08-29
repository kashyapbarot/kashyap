
from odoo import fields, models


class BarcodeRule(models.Model):
    _inherit = "barcode.rule"

    generate_model = fields.Selection(selection_add=[("product.product", "Products")])
