# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar

# Para debuguear
import logging

_logger = logging.getLogger(__name__)
# _logger.warning("----------------------------" + str(r.invoice_id))




# new field on Product.Template
class domain(models.Model):
    _name = 'product.template'
    _inherit ='product.template'

    subscription_days = fields.Integer(string='Días hasta caducidad')

class campo_calculado(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    campoCalculado = fields.Integer(string='Días que han pasado',compute="_campocalculado",store=False)
    rel_field = fields.Integer(string='Fecha Caducidad Establecida',related='product_id.subscription_days')
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


class revisando_factura_clientes(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    
    @api.model
    def revisando_factura_clientes(self):
        clientes = self.search([])
        
        # _logger.warning("--ArrayClientes--------------------------" + str(clientes))
        for r in clientes:
            # _logger.warning("--NombreClientes--------------------------" + str(r.name)+ ":" + str((r.invoice_ids)))
            # _logger.warning("--idFacturas--------------------------" + str(type(r.invoice_ids)))

            facturas = r.invoice_ids
            listaProductos = []
            # diccionario = {}
            diccionario = dict()
            fecha = datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S")
            for t in facturas:
                _logger.warning("--idFactura--------------------------" + str(t.id))
                # _logger.warning("--idFactura--------------------------" + str(t.create_date))

                # _logger.warning("--LineasFactura--------------------------" + str(t.invoice_line_ids))
                linea = t.invoice_line_ids
                _logger.warning("--linea--------------------------" + str(len(linea)))
                
                
                for j in linea:
                    _logger.warning("--idProducto--------------------------" + str(j.product_id.id))
                    ale = j.rel_field - ((datetime.now() - datetime.strptime(j.create_date, '%Y-%m-%d %H:%M:%S')).days)
                    if (ale<=30):
                        listaProductos.append(j.product_id.id)
                        diccionario = {1: j.product_id.name,
                                        2: j.product_id,
                                        3: j.quantity,
                                        4: 0.00,}#line.get('discount'),}
            self.create_sales_order( diccionario, r.id)
    @api.model
    def create_sales_order(self, orderline, customer_id):
        for g in orderline:
            _logger.warning("--ggggggggg--------------------------"+str(g)+"\n"+str(type(g)))
        _logger.warning("--Legueeee--------------------------")
        _logger.warning("--orderLine--------------------------"+str(orderline)+"\n"+str(type(orderline)))
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
                    #'signature': sign}
            _logger.warning("--SaleDiccionario--------------------------" + str(type(sale)))
            sale_id = sale_pool.create(sale)
            if sale_id:
                sale_brw = sale_id
                sale_brw.onchange_partner_id()
                #create sale order line
                for line in orderline:
                    _logger.warning("--LineaFor--------------------------" + str(line))
                    _logger.warning("--LineaTypeLine--------------------------" + str(type(line)))
                    sale_line = {}
                    # _logger.warning("--LineaGet--------------------------" + str(type(line.get('product_id'))))
                    #if line.get('product_id'):
                    #prod_rec = prod_pool.browse(line['product_id'])
                    prod_rec = orderline.get(2)
                    if prod_rec:
                    # orderLine.get
                        sale_line.update({'name': prod_rec.name or False,
                                        'product_id': prod_rec.id,
                                        'product_uom_qty': orderline.get(3),
                                        'discount':  orderline.get(4),
                                        'order_id': sale_id.id})
                        sale_line_id = sale_line_pool.create(sale_line)
                    for line in sale_line_id:
                        line.product_id_change()
        return {"name": sale_brw.name, "id": sale_brw.id } 




