# pylint: disable=missing-docstring
# Copyright 2020 AteneoLab
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Ateneo Payroll Commission',
    'summary': """
       Ateneo Payroll Commission.
       It calculates commissions based on invoiced values by employees within a period.
       """,
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'AteneoLab',
    'website': 'https://ateneolab.com',
    'depends': [
        'hr_payroll_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_payroll_data.xml',
        'views/employee_view.xml',
        'views/payroll_view.xml',
    ],
    'images': ['static/description/com_thumbnail.jpg',
               'static/description/icon.png',
               'static/description/logo.png',
               'static/src/img/comm-1.jpg',
               'static/src/img/1-commission.gif',
               'static/src/img/contract-1.jpg',
               'static/src/img/custom.jpg',
               'static/src/img/ecommerce.jpg',
               'static/src/img/einvoice.jpg',
               'static/src/img/emp-1.jpg',
               'static/src/img/Flag_of_Ecuador.jpg',
               'static/src/img/fleet.jpg',
               'static/src/img/medical-1.jpg',
               'static/src/img/payroll-1.jpg'],
    'price': 43.75,
    'currency': 'USD',
    'installable': True,
}
