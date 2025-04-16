# -*- coding: utf-8 -*-
{
    'name': 'Odoo Analyst',
    'version': '13.0.0.0',
    'summary': 'Odoo Analyst',
    'description': 'More insights, more power! our journey to 400 specialized Odoo analytics to all apps',
    'category': 'OdooSync',
    'author': 'Odoo Analyst',
    'website': 'https://odooanalyst.com',
    'depends': ['base', 'web'],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        # views
        'views/res_users.xml',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/client_actions/odoo_synk_iframe/odoo_synk_iframe.xml',
    ],
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
}
