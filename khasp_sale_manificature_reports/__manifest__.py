# -*- coding: utf-8 -*-
{
    'name': "khasp_sale_manificature_reports",

    'summary': """
        khasp""",

    'description': """
        this module print reports for models
        1- inspection.checklist
        2- tool.inspection
        3- repair.request
        4- design.request
    """,

    'author': "Mohamed Sabry",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'inspection_checklist_khasp', 'design_request_khasp', 'repair_request_khasp',
                'tool_inspection_khasp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/repair_request.xml',
        'reports/reports_tags.xml',
        'reports/tool_inspection.xml',
        'reports/inspection_checklist.xml',
        'reports/design_request.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
