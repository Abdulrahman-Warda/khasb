# -*- coding: utf-8 -*-
{
    'name': "khasp_hr_modification",

    'summary': """
        Khasp""",

    'description': """
        This module add work flow to 
        business_trip
        hr_extension
        hr_handover
        hr_leon
        hr_overtime
        hr_permission
        hr_resignation
        hr_termination
        hr_ticket
        hr_transfer
        hr_course
    """,

    'author': "Mohamed Sabry",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','marketme_saudi_hr_customize','termination_request','ohrms_loan','handover_request','extension_request','hr_course','hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/business_trip.xml',
        'views/hr_leon.xml',
        'views/hr_resignation.xml',
        'views/hr_transfer.xml',
        'views/hr_overtime.xml',
        'views/hr_permission.xml',
        'views/hr_ticket.xml',
        'views/hr_termination.xml',
        'views/hr_handover.xml',
        'views/hr_extension.xml',
        'views/hr_course.xml',
        'views/hr_leaves.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}