# -*- coding: utf-8 -*-
{
    'name': "khasp_hr_wizard_reports",

    'summary': """
        Khasp""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mohamed Sabry",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_punishment_allow'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/employee_disclosure.xml',
        'wizard/contract_trial_wizard.xml',
        'wizard/employee_age.xml',
        'wizard/employee_retirment.xml',
        'wizard/employee_joinning.xml',
        'wizard/contract_date.xml',
        'wizard/employee_retirment.xml',
        'wizard/employee_permission.xml',
        'wizard/employee_penalities.xml',
        'wizard/employee_insurance.xml',
        'reports/salary_advance_report.xml',
        'reports/contract_trial_report.xml',
        'reports/employee_age_report.xml',
        'reports/employee_retirment_report.xml',
        'reports/employee_joining_report.xml',
        'reports/contract_date_report.xml',
        'reports/employee_permission_report.xml',
        'reports/employee_penalities_report.xml',
        'reports/employee_insurance_report.xml',

        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}