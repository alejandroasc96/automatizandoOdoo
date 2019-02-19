# -*- coding: utf-8 -*-
{
    'name': "Automatizacion",

    'summary': """
        efren""",

    'description': """
       El proposito de este módulo es automatizar ciertas acciones de odoo.
    """,

    'author': "Alejandro",
    'website': "http://www.ale.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/automatizacion.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
    #],
}