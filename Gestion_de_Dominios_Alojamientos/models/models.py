# -*- coding: utf-8 -*-

from odoo import models, fields, api




class domain(models.Model):
    _name = 'product.product'
    _inherit ='product.product'

    deadLineDomain = fields.Datetime(string = 'fecha de caducidad')

class host(models.Model):
    _name = 'product.product'
    _inherit ='product.product'

    deadLineHost = fields.Datetime(string = 'fecha de caducidad')    

# class automatizacion(models.Model):
#     _name = 'automatizacion.automatizacion'

#     name = fields.Char(string="sirve esto?")
#     value = fields.Integer()


# class AccountInvoice(models.Model):
    # _name = 'account.invoice'
    # _inherit ='account.invoice'

    # def revision_due_invoices(self, id=None):
         
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
    