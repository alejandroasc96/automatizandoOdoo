# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class DeadLineTime(models.Model):
    _name = 'deadline'
    _rec_name = 'months'

    months = fields.Integer(string="months of services")


class Service(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    dead_line_service = fields.Many2one('deadline', string="Dead Line Service")


class StateListener(models.Model):
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
                line.date_to_end = datetime.now(
                ) + timedelta((line.product_id.dead_line_service.months * 30))
                pass
            pass

        return self.write({'state': 'open'})


class serviceInvoiceLine(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    date_to_end = fields.Date(string='Date To Die')
    days_to_end = fields.Integer(
        string='Days To Die', compute="_getDaysToDie", store=False)

    @api.one
    @api.depends('create_date')
    def _getDaysToDie(self):
        for line in self:
            if line.date_to_end == False:
                line.days_to_end = 0
                pass
            else:
                line.days_to_end = (datetime.strptime(
                    line.date_to_end, '%Y-%m-%d')-datetime.now()).days
                pass

    @api.model
    def _checkAllServices(self):
        clients = self.env['res.partner'].search([])
        for client in clients:
            if client.customer:
                lines = []
                for invoice in client.invoice_ids:
                    if invoice.state == 'paid' or invoice.state == 'open':
                        for invoiceLine in invoice.invoice_line_ids:
                            daysToEnd = (datetime.strptime(
                                invoiceLine.date_to_end, '%Y-%m-%d')-datetime.now()).days
                            if daysToEnd <= 30:
                                lines.append({1: invoiceLine.product_id.name,
                                              2: invoiceLine.product_id,
                                              3: invoiceLine.quantity,
                                              4: 0.00, })
                                pass
                            pass
                        pass
                    pass
                pass
                self.create_sales_order(lines, client.id)

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
            _logger.warning("1-------->"+str(sale))
            # crea saleorder, solo para la base d datos
            sale_id = sale_pool.create(sale)
            _logger.warning("2-------->"+str(sale_id))
            if sale_id:
                sale_id.onchange_partner_id()
        for lineOrder in linesOrder:
            # create sale order line
            sale_line = {}
            prod_rec = lineOrder.get(2)
            cantidad = lineOrder.get(3)
            _logger.warning("3-------->"+str(prod_rec))
            _logger.warning("4-------->"+str(cantidad))
            if prod_rec:
                sale_line = {'name': prod_rec.name or False,
                             'product_id': prod_rec.id,
                             'product_uom_qty': cantidad,
                             'discount':  lineOrder.get(4),
                             #  le dices quien es el padre
                             'order_id': sale_id.id}
                _logger.warning("5-------->"+str(sale_line))
                sale_line_id = sale_line_pool.create(sale_line)
                _logger.warning("6-------->"+str(sale_line_id))
        email_act = sale_id.action_quotation_send()
        _logger.warning("7-------->"+str(email_act))
        if email_act and email_act.get('context'):
            email_ctx = email_act['context']
            _logger.warning("8-------->"+str(email_ctx))
            email_ctx.update(default_email_from=sale_id.company_id.email)
            _logger.warning("9-------->"+str(_logger.warning))
            sale_id.with_context(email_ctx).message_post_with_template(
                email_ctx.get('default_template_id'))
            pass

        # sale_id.force_quotation_send()
        # return {"name": sale_id.name, "id": sale_id.id}
