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
            
            _logger.warning("--ArrayDeProductosQueTieneContratadoCliente--------------------------" + str(len(listaProductos)))

        # ------ Mi Generando Presupuesto --------
            vals = {
                        'partner_id': r.id,
                        # 'state': 'draft',
                        # # 'validity_date': date.today(),
                        # 'date_order': "2019-04-22 13:25:22",
                        # 'payment_term_id': r.invoice_id.payment_term_id.id,
                        # 'user_id': r.invoice_id.partner_id.user_id.name,
                        # 'company_id': r.invoice_id.user_id.company_id.id,
                        # 'partner_invoice_id': r.partner_id.id,
                        # 'partner_shipping_id': r.invoice_id.user_id.id,
                        # # 'template_id': 13,
                        'pricelist_id': 1,
                        
                        # 'order_policy': 'manual'
                                }
            mail_vals = {
                        'partner_id': r.id,
                        # 'state': 'draft',
                        # # 'validity_date': date.today(),
                        # 'date_order': fecha,
                        # 'payment_term_id': r.invoice_id.payment_term_id.id,
                        # 'user_id': r.invoice_id.partner_id.user_id.name,
                        # 'company_id': r.invoice_id.user_id.company_id.id,
                        # 'partner_invoice_id': r.partner_id.id,
                        # 'partner_shipping_id': r.invoice_id.user_id.id,
                        # # 'template_id': 13,
                        'pricelist_id': 1,
                        'product_id': listaProductos,
                        
                        # 'order_policy': 'manual'
                                }
            saletivo = self.env['sale.order']
            # new = saletivo.create(vals)
            # template_obj = self.env['mail.template'].search([('name','=','Ale')], limit=1)
            # Ale = template_obj.generate_email(mail_vals)
            # mail = self.env['mail.mail'].create(Ale)
            # mail.send(False,True)

            # ----Ejemplo de internet ,creando un pedido -------
            # for sale_order in self.browse(cr, uid, ids, context=context):
            # agreement = {
            #     'name': sale_order.name,
            #     'partner_id': sale_order.partner_id.id,
            #     'company_id': sale_order.company_id.id,
            #     'start_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            # }
            # agreement_id = agreement_obj.create(cr, uid, agreement,
            #                                     context=context)
            # agreement_ids.append(agreement_id)
            #     for order_line in sale_order.order_line:
            #         agreement_line = {
            #             'agreement_id': agreement_id,
            #             'product_id': order_line.product_id.id,
            #             'discount': order_line.discount,
            #             'quantity': order_line.product_uom_qty,
            #         }
            #         agreement_line_obj.create(cr, uid, agreement_line,
            #                                 context=context)

            # 2 Ejemplo internet
            @api.model
            def create_sales_order(self, orderline, customer_id, sign):
                sale_pool = self.env['sale.order']
                prod_pool = self.env['product.product']
                sale_line_pool = self.env['sale.order.line']
                sale_no = ''
                sale = {}
                if customer_id:
                    customer_id = int(customer_id)
                    sale = {'partner_id': customer_id, 
                            'partner_invoice_id': customer_id,
                            'partner_shipping_id': customer_id, 
                            'signature': sign}
                    sale_id = sale_pool.create(sale)
                    if sale_id:
                        sale_brw = sale_id
                        sale_brw.onchange_partner_id()
                        #create sale order line
                        for line in orderline:
                            sale_line = {}
                            if line.get('product_id'):
                                prod_rec = prod_pool.browse(line['product_id'])
                                sale_line.update({'name': prod_rec.name or False,
                                                'product_id': prod_rec.id,
                                                'product_uom_qty': line['qty'],
                                                'discount': line.get('discount'),
                                                'order_id': sale_id.id})
                                sale_line_id = sale_line_pool.create(sale_line)
                                for line in sale_line_id:
                                    line.product_id_change()
                return {"name": sale_brw.name, "id": sale_brw.id } 




