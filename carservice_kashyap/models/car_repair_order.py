# -*- coding: utf-8 -*-
"""Car Service Companies/workshops"""
from datetime import datetime
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.odoo import exceptions


class CarRepairOrder(models.Model):
    """table structure Car Repair Order"""
    _name = 'car.repair.order'
    _description = 'Car Repair Order'

    name = fields.Char(string='Subject', required=True)
    repair_number = fields.Char(string='Repair Number', required=True,
                                readonly=True,
                                default=lambda self: self.env[
                                    'ir.sequence'].next_by_code(
                                    'model.sequence'))
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle',
                              required=True)
    repair_type = fields.Many2one(comodel_name='repair.type',
                                  string='Repair Type',
                                  required=True)
    date = fields.Datetime(string='Date', required=False,
                           default=fields.Datetime.now)

    vehicle_status = fields.Selection(string='Vehicle ServiceStatus',
                                      selection=[('one', 'Under Guarantee'),
                                                 ('two',
                                                  'Not Under Guarantee'), ],
                                      required=False, )
    guarantee_type = fields.Selection(string='Guarantee type',
                                      selection=[('paid', 'Paid'),
                                                 ('free', 'Free'), ],
                                      required=False, )
    owner = fields.Many2one(comodel_name='res.partner', string='Owner',
                            required=True)
    # Address
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2", required=False)
    city = fields.Char(string="City", required=False, )
    zip = fields.Char(string="Zip", required=False, )
    country_id = fields.Many2one(comodel_name="res.country",
                                 string="Country", required=True,
                                 related='state_id.country_id',
                                 invisible=False, readonly=False,
                                 store=True)
    state_id = fields.Many2one(comodel_name="res.country.state",
                               string="State", required=False,
                               domain="[('country_id','=?',country_id)]")
    country_code = fields.Integer(string="Country Code",
                                  required=False,
                                  related='country_id.phone_code',
                                  store=True)
    # Personal Details
    phone = fields.Char(string="Phone", required=False, )
    email = fields.Char(string="Email", required=False, )
    tags = fields.Many2many(comodel_name='fleet.vehicle.tag', string='Tags')
    technician_id = fields.Many2one(comodel_name='res.users',
                                    string='Technician',
                                    required=False)
    service_manager = fields.Many2one(comodel_name='res.users',
                                      string='Service Manager',
                                      required=True)
    diagnosis_result = fields.Html(string='Diagnosis result', required=False)
    notes = fields.Text(string="Notes", required=False)
    total_order = fields.Integer(
            string='Total Repair order',
            required=False)

    _sql_constraints = [
        ('name', 'UNIQUE(repair_number)',
         'The  Repair Name must be unique !')
    ]

    # Constrains
    @api.constrains('phone')
    def constrains_phone(self):
        """Phone Validation"""
        for rec in self:
            if rec.phone:
                match = re.match(r'^[+]?([0-9]{2,4})?[\s]?[0-9]{10}$',
                                 str(rec.phone))
                if match is None:
                    raise ValidationError('Invalid Phone Number')

    @api.constrains('email')
    def constrains_mail(self):
        """Email Validation"""
        for rec in self:
            if rec.email:
                match = re.match(
                    r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    rec.email)
                if match is None:
                    raise ValidationError('Not a valid E-mail ID')

    # ONCHANGE ----------------
    @api.onchange('phone', 'country_code', 'state_id',
                  'country_id')
    def validate_phone(self):
        """Phone Number Check"""
        for rec in self:
            if rec.phone:
                # get last number(list) after space[eg.+91 2339 53->53]
                phone_number = f'{rec.phone}'.split()[-1]
                # check if number has 10 digit
                if len(phone_number) == 10:
                    # if user has country(code) available
                    # add (CODE with PHONE_NUMBER in field)
                    if rec.country_code:
                        rec.phone = f'+{rec.country_code} {phone_number}'
                    # if country(code) field is not available(or removed)
                    # add (PHONE_NUMBER in field)
                    elif rec.country_code == 0:
                        rec.phone = f'{phone_number}'
                # Check phone number format
                match = re.match(r'^[+]?([0-9]{2,4})?[\s]?[0-9]{10}$',
                                 str(rec.phone))
                if match is None:
                    raise ValidationError('Phone number invalid')

    @api.onchange('email')
    def validate_mail(self):
        """Email Check"""
        for rec in self:
            if rec.email:
                match = re.match(
                    r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    rec.email)
                if match is None:
                    raise ValidationError('Not a valid E-mail ID')

    states = fields.Selection(
        string='States',
        selection=[('one', 'Draft'),
                   ('two', 'Diagnosis'), ('three', 'Work in Progress'),
                   ('four', 'Done')],
        required=False, default='one')

    def draft_to_diagnosis(self):
        self.states = 'two'

    def wip_to_diagnosis(self):
        self.states = 'two'

    def diagnosis_to_wip(self):
        self.states = 'three'

    @api.model
    def create(self, vals):
        if self.env.user.has_group(
                'carservice_kashyap.service_manager_group_sub'):
            return super(CarRepairOrder, self).create(vals)
        else:
            raise exceptions.AccessError(
                _('Only Service Managers can create Repair Orders.'))

    def write(self, vals):
        if self.env.user.has_group(
                'carservice_kashyap.service_manager_group_sub'):
            return super(CarRepairOrder, self).write(vals)
        else:
            raise exceptions.AccessError(
                _('Only Service Managers can modify Repair Orders'))
