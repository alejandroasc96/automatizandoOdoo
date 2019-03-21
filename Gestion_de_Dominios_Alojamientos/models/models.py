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

class campo_calculado(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    # _inherit = 'product.template' #esto falla cuando lo activas

    campoCalculado = fields.Integer(string='Faltan estos días para que caduque',compute="_campocalculado")
    # referenciamos el campo fechaAle, que se encuentra en el modelo product.temple a account.invoice.line con el nombre que aparece a la izquierda
    
    rel_field = fields.Integer(string='fechaAlepp', related='product_id.fechaAle')
    funcionaFunciona = fields.Integer(string='eaeaeaeaeae')
    
    
    
    # _logger.warning("----------------------------" + str(reference_field_caducidad_producto)) 
    
    @api.depends('create_date')
    def _campocalculado(self):
        for r in self:
            r.campoCalculado = (datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days
            r.funcionaFunciona = r.campoCalculado - r.rel_field
            # Para debuguear
            # _logger.warning("----------------------------" + str(r.campoCalculado)) 

# class host(models.Model):
#     _name = 'product.product'
#     _inherit ='product.product'

#     deadLineHost = fields.Datetime(string = 'fecha de caducidad')    

# class automatizacion(models.Model):
#     _name = 'automatizacion.automatizacion'

#     name = fields.Char(string="sirve esto?")
#     value = fields.Integer()


# class AccountInvoice(models.Model):
    # _name = 'account.invoice'
    # _inherit ='account.invoice'

    # def revision_due_invoices(self, id=None):
    #  
    #     date_act = fields.Datetime.now()
    #     invoice_due_ids = self.search([('due_invoice','<=',date_act),
    #     ('state','=','open')])
    #     if invoice_due_ids:
    #         # Folios de Facturas Vencidas
    #         ref_list_due = [x.number for x in invoice_due_ids]
    #         from odoo import SUPERUSER_ID
    #         user_admin = self.env['res.user'].browse(SUPERUSER_ID)
    #         my_user = self.env.user
    #         mail_from = my_user.partner_id.email
    #         mail_to = user_admin.partner_id.email

    #         mail_vals = {
    #                 'subject': 'Notificacion de Facturas Vencidas %s' % date_act,
    #                 'author_id': my_user.id,
    #                 'email_from': mail_from,
    #                 'email_to': mail_to,
    #                 'message_type':'email',
    #                 'body_html': 'En la Fecha %s se encontraron las \
    #                 siguientes Facturas Vencidas %s' % (date_act, str(ref_list_due)) ,
    #                     }
    #         mail_id = self.env['mail.mail'].create(mail_vals)
    #         mail_id.send()
    