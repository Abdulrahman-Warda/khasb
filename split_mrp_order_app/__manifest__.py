# -*- coding: utf-8 -*-

{
    "name" : "Manufacturing Orders Splitting Apps",
    "author": "Edge Technologies",
    "version" : "12.0.1.0",
    "live_test_url":'https://youtu.be/SbjLA9-eiuY',
    "images":["static/description/main_screenshot.png"],
    'summary': 'Split MRP Splitting manufacturing Order Split Production Order Splitting manufacturing Splitting mrp Split manufacturing order line split mrp line manufacturing order separation partial manufacturing split process separate mrp line mrp split process',
    "description": """Split Manufacturing Order Odoo Apps use for split Manufacturing by number of quantity and by number of MO splitting from Current Order.
    """,
    "license" : "OPL-1",
    "depends" : ['mrp'],
    "data": [
            'security/allow_split_order.xml',
            'wizard/confirm_split_order.xml',
            'views/split_view.xml',      
    ],
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": 'EUR',
    'category': 'Manufacturing',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
