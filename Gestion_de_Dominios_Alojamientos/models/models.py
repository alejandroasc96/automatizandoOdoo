# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

import logging

_logger = logging.getLogger(__name__)
# _logger.warning("----------------------------" + str(r.invoice_id))
class stateListener(models.Model):
    _name = 'account.invoice'     
    _inherit = 'account.invoice'

    @api.onchange('state')
    def stateListener(self):
        _logger.warning("---------ENTRANDOSTATELISTENER-------------------")
        for line in self.search(['invoice_line_ids']):
            _logger.warning("---------DENTROFORRRR-------------------" + str(line.product_id.type))
            if line.product_id.type == 'service':
                _logger.warning("---------DENTRODELIFFFFFFF-------------------" + str(line.product_id.dead_line_service.months))
                line.date_to_end = datetime.strptime(
                    line.datetime.now(), '%Y-%m-%d %H:%M:%S') + timedelta((line.product_id.dead_line_service.months * 30)) 

        
class DeadLineTime(models.Model):
    _name = 'deadline'
    _rec_name = 'months'

    months = fields.Integer(string="months of services")

class serviceInvoiceLine(models.Model):
    _name = 'account.invoice.line'     
    _inherit = 'account.invoice.line'

    # days_to_end = fields.Integer(string='Days To Die', compute="_getDaysToDie", store=False)
    date_to_end = fields.Date(string='Date To Die', store=True)

    # @api.depends('create_date')
    # def _getDaysToDie(self):

    #     for r in self:
    #         if r.product_id.type == 'service' and r.date_to_end != False:
    #             r.days_to_end =  (datetime.strptime(r.date_to_end, '%Y-%m-%d')-datetime.now()).days + 1
    #             pass
    #         else:
    #             r.days_to_end = 0

    # @api.one
    # @api.depends('create_date')
    # def _getDateToDie(self):
    #     for r in self:
    #         if r.product_id.type == 'service':
    #             r.date_to_end = datetime.strptime(
    #                 r.create_date, '%Y-%m-%d %H:%M:%S') + timedelta((r.product_id.dead_line_service.months * 30)) 
            
            

class Service(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    dead_line_service = fields.Many2one('deadline',  string="Meses a caducar")
    
    

class revisando_factura_clientes(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    @api.model
    def revisando_factura_clientes(self):
        clientes = self.search([])
        for r in clientes:
            if r.invoice_ids:
                facturas = r.invoice_ids
                _logger.warning("---------FacturasQueTiene-------------------" + str(facturas))
                _logger.warning("---------FacturasQueTiene-------------------" + str(type(facturas)))
                arrayDeDict = []
                diccionario = {}
                # fecha = datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S")
                for t in facturas:
                    if t.state == 'paid' or t.state == "open":
                        linea = t.invoice_line_ids
                        for j in linea:
                            if j.product_id.type == 'service':
                                expirationDate = (datetime.now() - datetime.strptime(j.date_to_end, '%Y-%m-%d')).days
                                if expirationDate <= 30:
                                    diccionario = {1: j.product_id.name,
                                                    2: j.product_id,
                                                    3: j.quantity,
                                                    4: 0.00,}
                                    arrayDeDict.append(diccionario)
                                    
                        self.create_sales_order( arrayDeDict, r.id)
            

    @api.model
    def create_sales_order(self, arrayDeDict, customer_id):
        sale_pool = self.env['sale.order']
        prod_pool = self.env['product.product']
        sale_line_pool = self.env['sale.order.line']
        sale_no = ''
        sale = {}
        if customer_id:
            customer_id = int(customer_id)
            sale = {'partner_id': customer_id, 
                    'partner_invoice_id': customer_id,
                    'partner_shipping_id': customer_id}
            sale_id = sale_pool.create(sale)
            if sale_id:
                sale_brw = sale_id
                sale_brw.onchange_partner_id()
        for lineOrder in arrayDeDict:
            #create sale order line
            sale_line = {}
            prod_rec = lineOrder.get(2)
            cantidad = lineOrder.get(3)
            if prod_rec:
                sale_line = {'name': prod_rec.name or False,
                                'product_id': prod_rec.id,
                                'product_uom_qty': cantidad,
                                'discount':  lineOrder.get(4),
                                'order_id': sale_id.id}
                sale_line_id = sale_line_pool.create(sale_line)
        send_sale_order = sale_id.force_quotation_send()
        return {"name": sale_brw.name, "id": sale_brw.id } 
    


class review_quotation(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    @api.model
    def review_quotation(self):
        #search quotations how has state = sent (sent quotation)
        quotation = self.search([('state', 'in', ['sent'])]) 

        for quo in quotation:
            date = (datetime.now() - datetime.strptime(quo.date_order, '%Y-%m-%d %H:%M:%S')).days
            _logger.warning("--SentQuotation--------------------------" + str(date))
            
        #enviar mensaje a al canal
        # group = self.env['res.groups'].search([('category_id.name', '=', 'Manufacturing')])
        # recipient_partners = [1,6]
        # # for recipient in group.users: 
        # #     recipient_partners.append(
        # #         (4, recipient.partner_id.id)
        # #     )
        # _logger.warning("--aquienenvia--------------------------" + str(recipient_partners))
        # post_vars = {'subject': "notification about order",
        #     'body': "Yes inform me as i belong to manfacture group",
        #     'partner_ids': [1],} # Where "4" adds the ID to the list 
        # #                             # of followers and "3" is the partner ID 
        # # thread_pool = self.pool.get('mail.thread')
        # # thread_pool.message_post(self,
        # #         **post_vars)
        # body = "My Message!"
        # pepe = self.env['mail.channel']
        # pepe.message_post(post_vars)
        chanel = self.env['mail.channel']
        channel_id = self.env['ir.model.data'].xmlid_to_object('sb_medical_assistance_records.channel_sb_1')
        channel_id.message_post(
                        subject='SnippetBucket Technologies',
                        body='''Hi... Tejaskumar Tank, SnippetBucket.com''',
                        subtype='mail.mt_comment')

        


            # ale = self.env['mail.thread']
            # ale.message_post(body='<p>hola</p>', partner_ids=[1, 6])

# import subprocess

#     def sendmessage(message):
#     subprocess.Popen(['notify-send', message])
#     return


