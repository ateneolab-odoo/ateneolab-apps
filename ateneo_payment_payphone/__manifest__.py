# -*- coding: utf-8 -*-
{
    'name': "Payphone payment acquirer",
    'summary': """
        Payphone payment acquirer""",
    'description': """
        Payphone payment acquirer
    """,
    'author': "AteneoLab",
    'website': "https://ateneolab.com",
    'category': 'Payment method',
    'version': '14.0.1.0.0',
    'depends': ['base', 'payment', 'website_sale'],
    'price': '48.75',
    'currency': 'USD',
    'images': [
        'static/description/_thumbnail.jpg',
        ],
    'data': [
        'data/data.xml',
        'static/src/xml/assets.xml',
        'views/acquirer.xml',
        'views/templates.xml',
    ],
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
