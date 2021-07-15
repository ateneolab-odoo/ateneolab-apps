# -*- coding: utf-8 -*-

{
    'name': 'Kushki Payment Acquirer',
    'category': 'eCommerce',
    'summary': 'Payment Acquirer: Kushki Implementation',
    'version': '14.0.1.0.0',
    'description': """Kushki Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_kushki_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'license': 'AGPL-3',
    'author': 'AteneoLab',
    'website': 'https://ateneolab.com',
    'price': '116.66',
    'currency': 'USD',
    'images': [
        'static/description/kushki_thumbnail.jpg',
        'static/description/icon.png',
        'static/description/1pymnt.jpg',
        'static/description/1pymnt.jpg',
        'static/description/2atc.jpg',
        'static/description/3pnw.jpg',
        'static/description/4kajita.jpg',
        'static/description/5sccss.jpg',
        'static/description/1payment-method.gif',
        ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
