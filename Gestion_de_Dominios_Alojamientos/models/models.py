# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar

# Para debuguear
import logging

_logger = logging.getLogger(__name__)




class domain(models.Model):
    _name = 'product.template'
    _inherit ='product.template'

    subscriptionDays = fields.Integer(string='Días hasta caducidad')

class campo_calculado(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    campoCalculado = fields.Integer(string='Días que han pasado',compute="_campocalculado",store=False)
    # referenciamos el campo fechaAle, que se encuentra en el modelo product.temple a account.invoice.line con el nombre que aparece a la izquierda
    
    rel_field = fields.Integer(string='Fecha Caducidad Establcida',related='product_id.subscriptionDays')
    total = fields.Integer(string='Días restantes ',compute='_total',store=False)

    @api.one
    @api.depends('create_date')
    def _campocalculado(self):
        for r in self:
            r.campoCalculado = (datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days
            

    @api.one
    @api.depends('campoCalculado', 'rel_field')
    def _total(self):
        self.total = self.rel_field - self.campoCalculado 

class caducidad_productos(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    @api.model
    def caducidad_productos(self):
        total_dias = self.search([])
        print ("### Revisando las Facturas Vencidas")
        for r in total_dias:
            ale = r.rel_field - ((datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days)
            if (ale=30):
                mail_from = r.invoice_id.user_id.email
                mail_to = r.invoice_id.partner_id.email
                userID = r.invoice_id.user_id.id

                mail_vals = {
                            'subject': 'Notificacion de Facturas Vencidas',
                            'author_id': userID, #my_user.id,
                            'email_from': mail_from,
                            'email_to': mail_to,
                            'message_type':'email',
                            'body_html': 'Se te están caducadon las suscripciones',
                                }
                # template_obj = self.env['email.template'].sudo().search([('name','=','Create Section for Thesis')], limit=1)# Código Para Tiburcio
                mail_id = self.env['mail.mail'].create(mail_vals)
                mail_id.send()
                _logger.warning("----------------------------" + str(r.invoice_id))