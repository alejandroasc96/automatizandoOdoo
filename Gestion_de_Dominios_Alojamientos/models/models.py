# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class DeadLineTime(models.Model):
    _name = 'deadline'
    months = fields.Integer()


class Service(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    dead_line_service = fields.Many2one('deadline', string="Dead Line Service")
    days_to_end = fields.Integer(string='Days To Die', compute="_getDaysToDie", store=False)
    date_to_end = fields.Date(string='Date To Die',compute="_getDateToDie",store=True)

    @api.one
    @api.depends('create_date')
    def _getDaysToDie(self):
        for r in self:
            r.days_to_end = r.dead_line_service.months-(
                datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days
    
    @api.one
    @api.depends('create_date')
    def _getDateToDie(self):
        for r in self:
            total_days = 0
            for i in range(0, r.dead_line_service.months % 12):
                if datetime.now().month == 1:
                    total_days += 31
                if datetime.now().month == 2:
                    total_days += 28
                if datetime.now().month == 3:
                    total_days += 31
                if datetime.now().month == 4:
                    total_days += 30
                if datetime.now().month == 5:
                    total_days += 31
                if datetime.now().month == 6:
                    total_days += 30
                if datetime.now().month == 7:
                    total_days += 31
                if datetime.now().month == 8:
                    total_days += 31
                if datetime.now().month == 9:
                    total_days += 30
                if datetime.now().month == 10:
                    total_days += 31
                if datetime.now().month == 11:
                    total_days += 30
                if datetime.now().month == 12:
                    total_days += 31
            r.date_to_end = datetime.strptime(
                r.create_date, '%Y-%m-%d %H:%M:%S') + timedelta(total_days+(r.dead_line_service.months / 12*365))

    
            # r.dead_line_service.months-(
            #     datetime.now() - datetime.strptime(r.create_date, '%Y-%m-%d %H:%M:%S')).days            


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
