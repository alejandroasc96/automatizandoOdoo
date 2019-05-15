# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta


import logging

_logger = logging.getLogger(__name__)
# _logger.warning("----------------------------" + str(r.invoice_id))

class dateOrderFormat(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    date_order_format = fields.Date( string='Fecha formateada', compute="_getDateOrder", store=False)

    @api.model
    def _getDateOrder(self):
        saleOrder = self.search([])
        for line in saleOrder:
            x = line.date_order
            b = x[:10]
            line.date_order_format = b 



class DeadLineTime(models.Model):
    _name = 'deadline'
    _rec_name = 'months'

    months = fields.Integer(string="months of services")

class stateListener(models.Model):
    _name = 'account.invoice'     
    _inherit = 'account.invoice'
    

    @api.model
    @api.multi
    def invoice_validate(self):
        
        for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
            invoice.message_subscribe([invoice.partner_id.id])
        self._check_duplicate_supplier_reference()

        # code to calculate when the service from inoice.line will end
        for line in self.invoice_line_ids:
            if line.product_id.type == 'service':
                #Para calcular la fecha en la que caduca el servicio usamos el método relativedelta que nos va añadiendo
                #el número de meses que están estipulados.
                line.date_to_end = datetime.now() + relativedelta(months=line.product_id.dead_line_service.months)
                # line.only_date = datetime.strptime(line.date_to_end, '%Y-%m-%d')
                # _logger.warning("----------------------------" + str(line.only_date))
                pass
            pass

        return self.write({'state': 'open'})

class serviceInvoiceLine(models.Model):
    _name = 'account.invoice.line'     
    _inherit = 'account.invoice.line'

    date_to_end = fields.Date(string='Date To Die',store=True)
    # only_date = fields.Date(string='Date',store=True)
    days_to_end = fields.Integer(string='Days To Die', compute="_getDaysToDie", store=False)
    

    @api.depends('create_date')
    def _getDaysToDie(self):
        for line in self:
            if line.date_to_end==False:
                line.days_to_end = 0
                pass
            else:
                line.days_to_end =(datetime.strptime(line.date_to_end, '%Y-%m-%d')-datetime.now()).days + 1
                pass
            pass
            

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
                arrayDeDict = []
                diccionario = {}
                for t in facturas:
                    if t.state == 'paid' or t.state == "open":
                        linea = t.invoice_line_ids
                        for j in linea:
                            if j.product_id.type == 'service':
                                expirationDate = j.days_to_end
                                if expirationDate <= 31:
                                    diccionario = {1: j.product_id.name,
                                                    2: j.product_id,
                                                    3: j.quantity,
                                                    4: 0.00,}
                                    arrayDeDict.append(diccionario)
                                    
                self.create_sales_order( arrayDeDict, r.id)

    @api.model
    def create_sales_order(self, linesOrder, customer_id):
        sale_pool = self.env['sale.order']
        prod_pool = self.env['product.product']
        sale_line_pool = self.env['sale.order.line']
        # informacion de la factura generada
        sale = {}
        if customer_id:
            sale = {'partner_id': customer_id,
                    'partner_invoice_id': customer_id,
                    'partner_shipping_id': customer_id}
            # crea saleorder, solo para la base d datos
            sale_id = sale_pool.create(sale)
            if sale_id:
                sale_id.onchange_partner_id()
        for lineOrder in linesOrder:
            # create sale order line
            sale_line = {}
            prod_rec = lineOrder.get(2)
            cantidad = lineOrder.get(3)
            if prod_rec:
                sale_line = {'name': prod_rec.name or False,
                            'product_id': prod_rec.id,
                            'product_uom_qty': cantidad,
                            'discount':  lineOrder.get(4),
                            #  le dices quien es el padre
                            'order_id': sale_id.id}
                sale_line_id = sale_line_pool.create(sale_line)
        # añadiendo el attachment
        email_act = sale_id.action_quotation_send()
        if email_act and email_act.get('context'):
            email_ctx = email_act['context']
            email_ctx.update(default_email_from=sale_id.partner_id.email)
            sale_id.with_context(email_ctx).message_post_with_template(
                email_ctx.get('default_template_id'))
            pass


class review_quotation(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.model
    def review_quotation(self):
        quotation = self.search([('state', 'in', ['sent'])])
        for quo in quotation:
            date = (datetime.now() - datetime.strptime(quo.date_order, '%Y-%m-%d %H:%M:%S')).days
            _logger.warning("----------------------------" + str(date))
            if date <=30:
                
                self._postDeniedOrder({"quotation_id" : quo.id, "partner_id": quo.partner_id.name})

#enviar mensaje a Channel
    @api.model
    def _postDeniedOrder(self, order):
        
        channels = self.env['mail.channel'].search([])
        for channel in channels:
            if channel.name == "Denied Orders":
                _logger.warning("----------------------------" + str(order.get("quotation_id")))
                body = "Factura : " + str(order.get("quotation_id")) + " Cliente :" + str(order.get("partner_id"))
                channel.message_post(subject="order denied", body= body , subtype="mail.mt_comment")
                


