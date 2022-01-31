# -*- coding: utf-8 -*-
{
    'name': "khasp_sale_invoice_purchase_reports",

    'summary': """
        Khasp""",

    'description': """
        this module add (Governmental, private) customer quotation report
        add Governmental customer invoice report
        add purchase report
    """,

    'author': "Mohamed Sabry",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/partner.xml',
        'views/sale.xml',
        'views/invoice_view.xml',
        'views/purchase_view.xml',
        'views/company.xml',
        'views/templates.xml',
        'reports/reports.xml',
        'reports/quotation.xml',
        'reports/purchase.xml',
        'reports/invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}