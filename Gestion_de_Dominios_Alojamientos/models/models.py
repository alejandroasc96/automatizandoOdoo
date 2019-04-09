# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

import logging

_logger = logging.getLogger(__name__)

class DeadLineTime(models.Model):
    _name = 'deadline'
    months = fields.Integer(string="months of services")

class serviceInvoiceLine(models.Model):
    _name = 'account.invoice.line'     
    _inherit = 'account.invoice.line'
    days_to_end = fields.Integer(string='Days To Die', compute="_getDaysToDie", store=False)
    date_to_end = fields.Date(string='Date To Die',compute="_getDateToDie",store=True)
    @api.one
    @api.depends('create_date')
    def _getDaysToDie(self):
        for r in self:
            r.days_to_end = (datetime.strptime(
                r.date_to_end, '%Y-%m-%d')-datetime.now()).days

    @api.one
    @api.depends('create_date')
    def _getDateToDie(self):
        for r in self:
            r.date_to_end = datetime.strptime(
                r.create_date, '%Y-%m-%d %H:%M:%S') + timedelta(r.product_id.dead_line_service.months * 30)
            

class Service(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    dead_line_service = fields.Many2one('deadline', string="Dead Line Service")
    
    

    


