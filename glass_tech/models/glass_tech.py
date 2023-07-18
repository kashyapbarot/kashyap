# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    agreement_number = fields.Integer(
        string='Agreement Number',
        required=False)
    date_of_agreement = fields.Date(
        string='Date of Agreement',
        required=False)
    account_manager = fields.Selection(
        string='Account Manager',
        selection=[('Julie_dolens', 'Julie Dolens'),
                   ('george_varga', 'George Varga'),
                   ('select', '--Please Select--')],
        required=False, default='select')
    name_of_reference = fields.Char(
        string='Name of Reference',
        required=False)
    additional_notes = fields.Text(
        string="Additional Notes",
        required=False)
    special_instructions = fields.Text(
        string="SPECIAL INSTRUCTIONS",
        required=False)
    scope_of_work = fields.Text(
        string="SCOPE OF WORK",
        required=False)
    referral_source = fields.Selection(
        string='Referral Source',
        selection=[('Gt', 'GTrestore.com'),
                   ('google', 'Google'),
                   ('bing', 'Bing'),
                   ('other', 'Other Search Engin'),
                   ('social', 'Social Midea'),
                   ('business', 'Business Associate'),
                   ('family', 'Family/Friend'),
                   ('television', 'Television'),
                   ('radio', 'Radio'),
                   ('mail', 'Direct Mail'),
                   ('select', '--Please Select--')],
        required=False, default='select')


class ResPartner(models.Model):
    _inherit = "res.partner"

    preferred_method_of_contact = fields.Selection(
        string='Preferred Meth of Contact',
        selection=[('telephone', 'Telephone'),
                   ('email', 'Email'), ('text_sms', 'Text/SMS'),
                   ('standard_mail', 'Standard Mail'), ('other', 'Other'),
                   ('select', '--Please Select--')],
        required=False, default='select')
