# -*- coding: utf-8 -*-
from odoo import http

# class Automatizacion(http.Controller):
#     @http.route('/automatizacion/automatizacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automatizacion/automatizacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('automatizacion.listing', {
#             'root': '/automatizacion/automatizacion',
#             'objects': http.request.env['automatizacion.automatizacion'].search([]),
#         })

#     @http.route('/automatizacion/automatizacion/objects/<model("automatizacion.automatizacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automatizacion.object', {
#             'object': obj
#         })