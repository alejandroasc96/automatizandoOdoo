# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

import logging

_logger = logging.getLogger(__name__)

class DeadLineTime(models.Model):
    _name = 'deadline'
    months = fields.Integer( string="months of services", store=True)

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

    dead_line_service = fields.Many2one('deadline', string="Caduca en :", store=True)
    
    

class revisando_factura_clientes(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    @api.model
    def revisando_factura_clientes(self):
        clientes = self.search([])
        for r in clientes:
            facturas = r.invoice_ids
            arrayDeDict = []
            diccionario = {}
            fecha = datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S")
            for t in facturas:
                linea = t.invoice_line_ids
                for j in linea:
                    ale = j.rel_field - ((datetime.now() - datetime.strptime(j.create_date, '%Y-%m-%d %H:%M:%S')).days)
                    if (ale<=30):
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
            _logger.warning("--SentQuotation--------------------------" + str(quo))
            #enviar mensaje a user
            ale = self.env['mail.thread']
            ale.message_post(body='<p>hola</p>', partner_ids=[1, 6])


