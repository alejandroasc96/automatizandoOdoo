# -*- coding: utf-8 -*-
from odoo import http

# class GestionServicios(http.Controller):
#     @http.route('/gestion_servicios/gestion_servicios/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_servicios/gestion_servicios/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_servicios.listing', {
#             'root': '/gestion_servicios/gestion_servicios',
#             'objects': http.request.env['gestion_servicios.gestion_servicios'].search([]),
#         })

#     @http.route('/gestion_servicios/gestion_servicios/objects/<model("gestion_servicios.gestion_servicios"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_servicios.object', {
#             'object': obj
#         })