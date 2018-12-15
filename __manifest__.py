# -*- coding: utf-8 -*-
{
    'name': "Loans",
    'summary': """Loan Management System""",
    'author': "Haresh Kansara",
    'website': "http://www.jupical.com",
    'category': 'Loan Management',
    'version': '1.0',
    'depends': ['crm','mail', 'contacts'],
    'data': [
        'security/loan_management_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/mail_template.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}