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
    
    rel_field = fields.Integer(string='Fecha Caducidad Establecida',related='product_id.subscriptionDays')
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
            if (ale<=30):
                mail_from = r.invoice_id.user_id.email
                mail_to = r.invoice_id.partner_id.email
                userID = r.invoice_id.user_id.id

                mail_vals = {
                            'subject': 'Notificacion de Facturas Vencidas',
                            'author_id': userID,
                            'email_from': mail_from,
                            'email_to': mail_to,
                            'message_type':'email',
                            'body_html': 'Se te están caducadon las suscripciones',
                                }
                template_obj = self.env['mail.template'].search([('name','=','Tiburcio')], limit=1) # Código Para Tiburcio
            #     email_ids.append(self.pool.get('mail.mail').create(cr, uid, vals, context=context))
            # if email_ids:
            #     self.pool.get('mail.mail').send(cr, uid, email_ids, context=context)
                # mail_id = self.env['mail.mail'].create(mail_vals)
                # mail_id.send()
                template_obj.generate_mail(r.id)
                mail_id = self.env['mail.mail'].create(template_obj)
                # _logger.warning("----------------------------" + str(r.invoice_id))

        # def send_email(self,cr,uid,ids,context=None):
        #     template_obj = self.pool.get('mail.template')
        #     ir_model_data = self.pool.get('ir.model.data')
        #     # Create a template id by either of the ways.
        #     #template_id = template_obj.create(cr, uid,{'name':'Template Name','model_id':'Your model id'})
        #     template_id= ir_model_data.get_object_reference(cr, uid, 'module_name', 'xml_template_id')[1]
        #     if template_id:
        #         #------------ if a template id is created -------------------
        #         values = template_obj.generate_email(cr, uid, template_id, ids[0], context=context)
        #         #  Set/Modify the values for the template.
        #         values['subject'] = subject you want to show
        #         values['email_to'] = receiver of the email
        #         values['partner_to'] = partner ids
        #         values['body'] = body_html
        #             .....
        #             .....
        #         #--------------------------------------------------------------
        #         #----------------if template id is not created-----------------
        #         values = {
        #         'subject': 'subect ',
        #         'body_html': 'Message to be sent',
        #         'email_to': receiver email,
        #         'email_from': 'sender_email',
        #         values['partner_to'] : partner ids
        #         ......
        #         ......
        #         }
        #     #---------------------------------------------------------------
        #     mail_obj = self.pool.get('mail.mail') 
        #     msg_id = mail_obj.create(cr, uid, values, context=context) 
        #     if msg_id: 
        #         mail_obj.send(cr, uid, [msg_id], context=context) 
        #     return True
    
    