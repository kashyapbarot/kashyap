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
        obj = obj_mrp.search([('user_id', '=', current_user_selected.id),
                              ('date_end', '=', None)])
        obj1 = obj_mrp.search_count(
            [('user_id', '=', current_user_selected.id),
             ('date_end', '!=', None)])
        # print("user records----------------",obj1)

        if not obj:
            action = \
                self.env.ref('test.action_custom_mrp_productivity').read()[0]
            # return {
            #     'name': 'create user',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'custom.mrp.wizard',
            #     'type': 'ir.actions.act_window',
            #     'target': 'new',
            #     'action_id': action.id,
            #     'context': {'default_date_start': datetime.now(),
            #                 'default_user_new_id': self.user_new_id.id},
            #
            # }
            action.update({'views': [[False, 'form']],
                           'context': {'default_date_start': datetime.now(),
                                       'default_user_new_id': self.user_new_id.id}})
            return action

        elif obj and obj.date_start and not obj.date_end:
            date_start = obj.date_start
            action = \
                self.env.ref('test.action_custom_mrp_productivity').read()[0]
            # return {
            #     'name': 'user log out',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'action_id': action.id,
            #     'res_model': 'custom.mrp.wizard',
            #     'type': 'ir.actions.act_window',
            #     'target': 'new',
            #     'context': {'default_date_start': date_start,
            #                 'default_date_end': datetime.now(),
            #                 'default_user_new_id': self.user_new_id.id},
            #
            # }
            action.update({'views': [[False, 'form']],
                           'context': {'default_date_start': date_start,
                                       'default_date_end': datetime.now(),
                                       'default_user_new_id': self.user_new_id.id}})
            return action

    def check_start_date(self):
        current_user_selected = self.user_new_id
        obj_mrp = self.env['mrp.workcenter.productivity']
        obj = obj_mrp.search([('user_id', '=', current_user_selected.id),
                              ('date_end', '=', None)])
        workcenter = self.env.ref('mrp.mrp_workcenter_3').id
        workcenter_loss = self.env.ref('mrp.block_reason6').id

        if not obj:
            obj_mrp.create({'workcenter_id': workcenter,
                            'date_start': self.date_start,
                            'user_id': self.user_new_id.id,
                            'loss_id': workcenter_loss,
                            })
        elif obj:
            for rec in obj:
                obj = rec
            if obj and obj.date_start and not obj.date_end:
                self.date_start = obj.date_start
                self.user_new_id = self.user_new_id
                obj.write({'date_end': self.date_end})
