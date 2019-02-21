# -*- coding: utf-8 -*-
{
    'name': "Gestión de Dominios/Alojamientos",

    'summary': """
        Herramienta para la gestión de los dominios / alojamientos 
        (y productos relacionados) de los clientes.
        """,

    'description': """        
            - Genera automáticamente el presupuesto en una fecha previa al vencimiento del producto.
            - Envía por email el presupuesto.
            - Generación de la correspondiente factura cuando corresponda en caso de aprobación del presupuesto.
    """,

    'author': "Alejandro y Bryan",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': 'True',
}