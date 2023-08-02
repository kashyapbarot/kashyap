# -*- coding: utf-8 -*-
"""Manufacturing Model"""

from datetime import datetime, timedelta
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
        """ check user in productivity list """
        current_user_selected = self.user_new_id
        obj_mrp = self.env['mrp.workcenter.productivity']
        obj = obj_mrp.search([('user_id', '=', current_user_selected.id),
                              ('date_end', '=', None)])
        if not obj:
            action = \
                self.env.ref('test.action_custom_mrp_productivity').read()[0]
            action.update({'views': [[False, 'form']],
                           'context': {'default_date_start': datetime.now(),
                                       'default_user_new_id': self.user_new_id.id}})
            return action
        elif obj:
            for rec in obj:
                if rec and rec.date_start and not rec.date_end:
                    date_start = rec.date_start
                    action = \
                        self.env.ref(
                            'test.action_custom_mrp_productivity').read()[0]
                    action.update({'views': [[False, 'form']],
                                   'context': {
                                       'default_date_start': date_start,
                                       'default_date_end': datetime.now(),
                                       'default_user_new_id': self.user_new_id.id}})
                    return action

    def check_start_date(self):
        """" set equal time for multiple  record with same user """
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
            check_open_rec = self.env[
                'mrp.workcenter.productivity'].search_count(
                [('user_id', '=', current_user_selected.id),
                 ('date_end', '=', None)])
            obj.write({'date_end': self.date_end})
            start_date = obj.mapped('date_start')
            end_date = obj.mapped('date_end')
            new_start_date = min(start_date)
            start_date_list = [time.time() for time in start_date]
            end_date_list = [time.time() for time in end_date]
            start_date_time = min(start_date_list)
            end_date_time = max(end_date_list)
            start = datetime.strptime(str(start_date_time), "%H:%M:%S")
            end = datetime.strptime(str(end_date_time), "%H:%M:%S")
            difference = end - start
            total_seconds = (difference.total_seconds()) / check_open_rec
            for rec in obj.sorted(key='date_start'):
                end_date = new_start_date + timedelta(seconds=total_seconds)
                rec.write({'date_end': end_date, 'date_start': new_start_date})
                new_start_date = end_date

