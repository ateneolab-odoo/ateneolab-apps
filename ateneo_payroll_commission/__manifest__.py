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
               'static/description/banner_screenshot.jpg',
               'static/description/comm-1.jpg',
               'static/description/1-commission.gif',
               'static/description/contract-1.jpg',
               'static/description/custom.jpg',
               'static/description/ecommerce.jpg',
               'static/description/einvoice.jpg',
               'static/description/emp-1.jpg',
               'static/description/Flag_of_Ecuador.jpg',
               'static/description/fleet.jpg',
               'static/description/medical-1.jpg',
               'static/description/payroll-1.jpg'],
    'price': 43.75,
    'currency': 'USD',
    'installable': True,
}
