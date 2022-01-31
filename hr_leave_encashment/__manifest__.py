# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Leave Encashment',
    'summary': """""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Abdulrahman Warda',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll',
        'hr_holidays',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_leave_encashment.xml',
        'data/hr_salary_rule.xml',
    ],
}
