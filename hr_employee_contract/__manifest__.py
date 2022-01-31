# -*- coding: utf-8 -*-
{
    'name': "Hr Employee Contract - Diar",

    'summary':"Diar Project",
    'description': """        
        - edit contract 
    """,

    'author': "Marketme-it",

    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_contract','project','hr_holidays','hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/hr_holiday_security.xml',
        'wizards/assign_employess_view.xml',
        'wizards/insurance_report.xml',
        'views/hr_contract.xml',
        'views/hr_contract_settings.xml',
        'views/hr_leave.xml',
        'views/hr_employee.xml',
        'views/project.xml',
        'views/report_insurance.xml',
        'data/hr_contract_cron.xml',
        'data/hr_contract_email.xml',
    ],
}