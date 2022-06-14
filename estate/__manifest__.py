# -*- coding: utf-8 -*-

{
    'name': "Real Estate Advertisement",
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/estate_property_views.xml',
        'data/estate_menus.xml'
        ],
    'author': "Alexa Acosta",
    'category': 'Marketing',
    'license': 'OPL-1',
    'description': """
        Lists all Real Estate advertisements and associated information.
    """,
    'application': True,
    'installable': True,
    'auto_install': False
}
