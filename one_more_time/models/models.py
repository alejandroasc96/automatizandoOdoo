# -*- coding: utf-8 -*-

from odoo import models, fields, api

class one_more_time(models.Model):
    _name = 'product.product'

    pepinillos = fields.Integer(string = "aserejesito")

    def _value_pc(self):
        self.pepinillos = float(self.value) / 100
        log (self.pepinillos)