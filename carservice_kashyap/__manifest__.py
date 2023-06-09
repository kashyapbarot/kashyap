# -*- coding: utf-8 -*-

{
    'name': 'Carservice Kashyap',
    'version': '1.2',
    'summary': 'Car Service Companies',
    'description': 'Car Service Companies Module',
    'category': 'Product Manufacturer',
    'author': 'Kashyap',
    'license': 'LGPL-3',
    'depends': ['base', 'fleet', 'sale'],
    'data': ['security/res_groups.xml', 'security/ir.model.access.csv',
             'data/auto_sequence.xml', 'wizard/car_repair_order_wizard.xml',
             'data/repair_data.xml', 'report/car_repair_order.xml',
             'views/car_master_view.xml',
             'views/car_repair_order_view.xml', 'views/repair_type.xml',
             'views/sale_order.xml',
             'views/menu_record.xml'
             ],
    'installable': True,
    'auto_install': False,
}
