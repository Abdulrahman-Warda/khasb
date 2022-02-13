# -*- coding: utf-8 -*-
{
    'name': "hr_reporting",

    'summary': """""",

    'description': """""",

    'author': "Abdulrahman Warda",

    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base', 'hr'],

    'data': [
        'views/views.xml',
        'reports/report_actions.xml',
        'reports/report_templates.xml',
        'data/ir_sequence.xml',
    ],
}
