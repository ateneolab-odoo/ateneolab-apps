# pylint: disable=missing-docstring
# Copyright 2020 AteneoLab
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Ateneo Payroll Commission',
    'summary': """
       Ateneo Payroll Commission.
       It calculates commissions based on invoiced values within a period.
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
               'static/description/banner_screenshot.png',
               'static/description/comm-1.png',
               'static/description/1-commission.gif',
               'static/description/contract-1.png',
               'static/description/custom.png',
               'static/description/ecommerce.png',
               'static/description/einvoice.png',
               'static/description/emp-1.png',
               'static/description/Flag_of_Ecuador.svg',
               'static/description/fleet.png',
               'static/description/medical-1.png',
               'static/description/payroll-1.png'],
    'price': 43.75,
    'currency': 'USD',
    'installable': True,
}
