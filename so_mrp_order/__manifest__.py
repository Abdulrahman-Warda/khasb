# -*- coding: utf-8 -*-

{
    'name': 'Make MRP orders from So',
    'version': '12.0.2.0.0',
    'summary': """Launch Automatic MRP Orders After Selling Through So.""",
    'description': """Launch automatic MRP orders after selling through So""",
    'category': 'Point of Sale',
    'depends': ['sale', 'mrp', 'stock'],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
