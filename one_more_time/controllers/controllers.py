# -*- coding: utf-8 -*-
from odoo import http

# class OneMoreTime(http.Controller):
#     @http.route('/one_more_time/one_more_time/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_more_time/one_more_time/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_more_time.listing', {
#             'root': '/one_more_time/one_more_time',
#             'objects': http.request.env['one_more_time.one_more_time'].search([]),
#         })

#     @http.route('/one_more_time/one_more_time/objects/<model("one_more_time.one_more_time"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_more_time.object', {
#             'object': obj
#         })