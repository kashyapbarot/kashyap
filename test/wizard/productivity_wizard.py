# -*- coding: utf-8 -*-
"""Product Manufacturer Model"""

from datetime import datetime
from odoo import models, fields, api


class CustomSaleOrder(models.TransientModel):
    """Wizard Class"""
    _name = 'custom.mrp.wizard'
    _description = 'custom mrp workcenter productivity wizard'

    check_productivity_id = fields.Many2one(
        comodel_name='mrp.workcenter.productivity',
        string='Record', )
    user_new_id = fields.Many2one(
        comodel_name='res.users',
        string='User id',
        required=True)

    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')

    is_end_date = fields.Boolean(
        string='Is date',
        required=False)

    def check_user(self):
        current_user_selected = self.user_new_id
        obj_mrp = self.env['mrp.workcenter.productivity']
        obj = obj_mrp.search([('user_id', '=', current_user_selected.id)])
        if not obj:
            view_id = self.env.ref('test.view_custom_productivity_wizard_form').id
            return {
                'name': 'create user',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(view_id, 'form')],
                'res_model': 'custom.mrp.wizard',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {'default_date_start': datetime.now(),
                            'default_user_new_id': self.user_new_id.id, 'context': self._context},

            }
        elif obj and obj.date_start and not obj.date_end:
            date_start = obj.date_start
            view_id = self.env.ref('test.view_custom_productivity_wizard_form').id
            return {
                'name': 'user log out',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(view_id, 'form')],
                'res_model': 'custom.mrp.wizard',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {'default_date_start': date_start,
                            'default_date_end': datetime.now(),
                            'default_user_new_id': self.user_new_id.id, 'context': self._context},

            }

    def check_start_date(self):
        current_user_selected = self.user_new_id
        obj_mrp = self.env['mrp.workcenter.productivity']
        obj = obj_mrp.search([('user_id', '=', current_user_selected.id)])
        workcenter = self.env.ref('mrp.mrp_workcenter_3').id
        workcenter_loss = self.env.ref('mrp.block_reason6').id
        if obj and obj.date_start and not obj.date_end:
            self.date_start = self.check_productivity_id.date_start
            self.user_new_id = self.user_new_id
            obj.write({'date_end': self.date_end})
        elif not obj:
            obj_mrp.create({'workcenter_id': workcenter,
                            'date_start': self.date_start,
                            'user_id': self.user_new_id.id,
                            'loss_id': workcenter_loss,
                            })
