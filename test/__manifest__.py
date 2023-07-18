# -*- coding: utf-8 -*-

{
    'name': 'test',
    'version': '1.2',
    'summary': 'Test',
    'description': "test product",
    'category': 'Property',
    'depends': ['crm', 'purchase', 'sale','mrp'],
    'data': ['security/ir.model.access.csv',
             'views/documents_custom_view.xml', 'views/customer_doc_tags_view.xml',
             'views/menu_root.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
}
