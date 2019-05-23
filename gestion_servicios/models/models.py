# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta


import logging

_logger = logging.getLogger(__name__)


class addDepartmentFieldResPartner(models.Model):
    
    _inherit = 'res.partner'

    department = fields.Char(string='Departamento')

# Fecha formateada para el PDF
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


# Duracion del servico en meses
class DeadLineTime(models.Model):
    _name = 'deadline'
    _rec_name = 'months'

    months = fields.Integer(string="months of services")


class stateListener(models.Model):
    _name = 'account.invoice'     
    _inherit = 'account.invoice'
    
# code to calculate when the service from inoice.line will end
    @api.model
    @api.multi
    def invoice_validate(self):
        
        for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
            invoice.message_subscribe([invoice.partner_id.id])
        self._check_duplicate_supplier_reference()

        
        for line in self.invoice_line_ids:
            if line.product_id.type == 'service':
                #Para calcular la fecha en la que caduca el servicio usamos el método relativedelta que nos va añadiendo
                #el número de meses que están estipulados.
                line.date_to_end = datetime.now() + relativedelta(months=line.product_id.dead_line_service.months)
                pass
            pass

        return self.write({'state': 'open'})

# Clase que añada dos nuevos campos a account.invoice.line
class serviceInvoiceLine(models.Model):
    _name = 'account.invoice.line'     
    _inherit = 'account.invoice.line'

    date_to_end = fields.Date(string='Date To Die',store=True)
    days_to_end = fields.Integer(string='Days To Die', compute="_getDaysToDie", store=False)
    
    # Se calculan dichos campos según condiciones
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
            

# Creacion de relacion entre producto y durancion del servicio
class Service(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    dead_line_service = fields.Many2one('deadline',  string="Meses a caducar")
    
    


class revisando_factura_clientes(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    # Revisando las caducidad de todos los servicios contratados por todos los clientes
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
                                # Falta comprobar que la línea de producto no haya sido enviada
                                if expirationDate <= 31 and expirationDate > 15:
                                    diccionario = {1: j.product_id.name,
                                                    2: j.product_id,
                                                    3: j.quantity,
                                                    4: 0.00,}
                                    arrayDeDict.append(diccionario)
                                    
                self.create_sales_order( arrayDeDict, r.id)

    # Creando el presupuesto a notificar al cliente por correo
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
        # Realizando el envio del presupuesto al cliente
        email_act = sale_id.action_quotation_send()
        # añadiendo el attachment
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
            # hay que comprobar que no haya sido notificado ya
            if date =15 and quo.state == 'sent':
                
                self._postDeniedOrder({"quotation_id" : quo.id, "partner_id": quo.partner_id.name})

#enviar notificacion a Channel del presupuesto sin respuesta
    @api.model
    def _postDeniedOrder(self, order):
        
        channels = self.env['mail.channel'].search([])
        for channel in channels:
            if channel.name == "Denied Orders":
                body = "Factura : " + str(order.get("quotation_id")) + " Cliente :" + str(order.get("partner_id"))
                channel.message_post(subject="order denied", body= body , subtype="mail.mt_comment")
                


