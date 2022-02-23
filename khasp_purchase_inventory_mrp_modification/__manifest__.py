# -*- coding: utf-8 -*-
{
    'name': "khasp_purchase_inventory_mrp_modification",

    'summary': """
        Khasp""",

    'description': """
        this module :
        1- add (factory manger, financial manger, general manger) states to purchase order
        2- add quality control before eny transaction operations
        3- add machine tool to every machine in mrp machine
        4-give domain to every worker to his work order
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','stock','sprogroup_purchase_request_khasb','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/workorder_rule.xml',
        'data/mail_template.xml',
        'wizard/quality_control.xml',
        'wizard/workorder_wizard.xml',
        'views/purchase.xml',
        'views/inventory.xml',
        'views/purchase_request.xml',
        'views/workorders_mrp.xml',
        'views/workcenter_mrp.xml',
        'views/product.xml',
        'views/templates.xml',
        'reports/report_actions.xml',
        'reports/report_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
