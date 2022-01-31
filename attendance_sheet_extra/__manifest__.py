# -*- coding: utf-8 -*-
{
    'name': "Hr Attendance Sheet Extra",

    'summary': """
        """,

    'description': """
    """,

    'author': "Eng.Ramadan Khalil",
    'website': "",

    'category': 'hr',
    'version': '12.0.0',

    'depends': ['base','hr_attendance_sheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/att_sheet_batch_view.xml',
        'views/attendance_sheet_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}