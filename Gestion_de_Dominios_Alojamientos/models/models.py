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

    fechaAle = fields.Integer(string='Días hasta caducidad')

    # state = fields.Selection([('30','1 mes'),('open','3 meses'), ('done','6 meses')],'State')

class campo_calculado(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    # _inherit = 'product.template' #esto falla cuando lo activas

    campoCalculado = fields.Integer(string='Días que han pasado',compute="_campocalculado",store=False)
    # referenciamos el campo fechaAle, que se encuentra en el modelo product.temple a account.invoice.line con el nombre que aparece a la izquierda
    
    rel_field = fields.Integer(string='Fecha Caducidad Establcida',related='product_id.fechaAle')
    total = fields.Integer(string='Días restantes ',compute='_total',store=False)

    
    # _logger.warning("----------------------------" + str(reference_field_caducidad_producto)) 
    # @api.one
    @api.depends('create_date')
    def _campocalculado(self):
        for r in self:
            r.campoCalculado = (datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days
            

            # r.funcionaFunciona = r.campoCalculado - r.rel_field
            # Para debuguear
            _logger.warning("--CampoCalculado1--------------------------" + str(r.campoCalculado))
            # self.total = self.campoCalculado - self.rel_field
            # _logger.warning("restaResta----------------------------" + str(self.total))
        _logger.warning("----CampoCalculado2------------------------" + str(r.campoCalculado)) 

    # @api.one
    @api.depends('campoCalculado', 'rel_field')
    def _total(self):
        self.total = self.rel_field - self.campoCalculado 
        _logger.warning("--total1--------------------------" + str(self.total))

class caducidad_productos(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    

    
    @api.model
    def caducidad_productos(self):
        # _logger.warning("----------------------------" + str(self))
        total_dias = self.search([])
        # _logger.warning("----------------------------" + str(total_dias))
        print ("### Revisando las Facturas Vencidas")
        for r in total_dias:
            # _logger.warning("----------------------------" + str(r.total))
            ale = r.rel_field - ((datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days)
            _logger.warning("----------------------------" + str(ale))
            if (ale<=30):
                from odoo import SUPERUSER_ID
                # user_admin = self.env['res.user'].browse(SUPERUSER_ID)
                # my_user = self.env.user
                mail_from = 'alejandroasc96@gmail.com'  #'alejandroasc96@gmail.com' order_id.partner_id.email
                mail_to = r.invoice_id.partner_id.email # my_user.partner_id.email #user_admin.partner_id.email #'alejandroasc96@gmail.com'

                mail_vals = {
                            'subject': 'Notificacion de Facturas Vencidas',
                            'author_id': 1, #my_user.id,
                            'email_from': mail_from,
                            'email_to': mail_to,
                            'message_type':'email',
                            'body_html': 'Se te están caducadon las suscripciones',
                                }
                mail_id = self.env['mail.mail'].create(mail_vals)
                mail_id.send()
                _logger.warning("----------------------------" + str(r.invoice_id))