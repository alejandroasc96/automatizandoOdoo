# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import smtplib
import logging



class automatizacion(models.Model):
    _name = 'product.product'
    _inherit ='product.product'

    deadLineDomain = fields.Datetime(string = 'fecha de caducidad')


# class AccountInvoice(models.Model):
#     _name = 'account.invoice'
#     _inherit ='account.invoice'

#     def revision_due_invoices(self, id=None):
         
#         date_act = fields.Datetime.now()
#         invoice_due_ids = self.search([('due_invoice','<=',date_act),
#         ('state','=','open')])
#         if invoice_due_ids:
#             # Folios de Facturas Vencidas
#             ref_list_due = [x.number for x in invoice_due_ids]
#             from odoo import SUPERUSER_ID
#             user_admin = self.env['res.user'].browse(SUPERUSER_ID)
#             my_user = self.env.user
#             mail_from = my_user.partner_id.email
#             mail_to = user_admin.partner_id.email

#             mail_vals = {
#                     'subject': 'Notificacion de Facturas Vencidas %s' % date_act,
#                     'author_id': my_user.id,
#                     'email_from': mail_from,
#                     'email_to': mail_to,
#                     'message_type':'email',
#                     'body_html': 'En la Fecha %s se encontraron las \
#                     siguientes Facturas Vencidas %s' % (date_act, str(ref_list_due)) ,
#                         }
#             mail_id = self.env['mail.mail'].create(mail_vals)
#             mail_id.send()

# Última fase de prueba
class informecorreo(models.Model):
    _name = 'informecorreo'

    #@api.model
    def enviar_informe_correo(self):
        try:
            print ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # total_empleados = self.env['hr.employee'].search_count([('department_id', '=', 4)])
            total_empleados = "ale"
            
            sender="odoo@micorreo.com"
            receiver=["tiburcio.cruz@gmail.com"]
            # asunto= "Informe semanal"
            # texto="Total de empleados en el departamento de Becarios: " + str(total_empleados)
            # message = """From: %s\nTo: %\nSubject: %s\n\n%s""" % (sender, ", ".join(receiver), asunto, texto)
            message = "hola"
            
            smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=465)
            smtpObj.ehlo()
            smtpObj.starttls()
            username="pushnotificationsmanager@gmail.com"
            pwd="AlejandroBryanInventia"
            smtpObj.login(user=username, password=pwd)
            smtpObj.sendmail(sender,receiver,message)
            smtpObj.quit()
            self.state='Enviando correo...'
            print ("Correo enviado")
        except smtplib.SMTPException:
            print ("Error al enviar el correo")

# Prueba de Prueba

class informecorreov2(models.Model):
    _name = 'informecorreov2'

    @api.model
    def enviar_informe_correov2(self):
        try:
            # total_empleados = self.env['hr.employee'].search_count([('department_id', '=', 4)])
            total_empleados = "ale"
            sender="odoo@micorreo.com"
            receiver=["alejandrosantana90@gmail.com"]
            asunto= "Informe semanal"
            texto="Total de empleados en el departamento de Becarios: " + str(total_empleados)
            message = """From: %s\nTo: %\nSubject: %s\n\n%s""" % (sender, ", ".join(receiver), asunto, texto)
            smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
            smtpObj.ehlo()
            smtpObj.starttls()
            username="pushnotificationsmanager@gmail.com"
            pwd="AlejandroBryanInventia"
            smtpObj.login(user=username, password=pwd)
            smtpObj.sendmail(sender,receiver,message)
            smtpObj.quit()
            self.state='Enviando correo...'
            print ("Correo enviado")
        except smtplib.SMTPException:
            print ("Error al enviar el correo")
    