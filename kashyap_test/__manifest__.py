# -*- coding: utf-8 -*-

{
    'name': 'kashyap product',
    'version': '1.2',
    'summary': 'Test',
    'description': "kashyap product",
    'category': 'Property',
    'depends': ['crm', 'purchase', 'sale', 'hr', 'attachment_indexation','stock','mrp'],
    'data': ['security/ir.model.access.csv','report/documents_custom_report.xml','views/do_report.xml', 'views/tag_id_inherit.xml',
             'views/product_product_gantt_view.xml','views/sale_order_list.xml','views/sale_order_search.xml',
             'views/employee_pivot_view.xml', 'views/sale_order_inherit.xml', 'views/delivery_view.xml',
             'views/documents_custom_view.xml','wizard/sale_order_wizard.xml', 'views/customer_doc_tags_view.xml', 'views/product_inherit.xml',
             'views/menu_root.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
}
