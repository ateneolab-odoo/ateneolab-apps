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
    'license': 'LGPL-3',
    'images': [
        'static/description/0-a1thumbnail_screenshot.png',
        'static/description/0-ateneo_screenshot.png',
        'static/description/1-payphone_acquirer_screenshot.png',
        'static/description/2-paynow_screenshot.png',
        'static/description/3-payphone_link_screenshot.png',
        'static/description/4-payphone_link1_screenshot.png',
        'static/description/5-payphone_link2_screenshot.png',
        'static/description/6-payphone_pay1_screenshot.jpeg',
        'static/description/7-payphone_pay_screenshot.jpeg',
        'static/description/8-payphone_pay2_screenshot.jpeg',
        'static/description/9-payphone_pay3_screenshot.jpeg',
        'static/description/1-payment_details_screenshot.png',
        'static/description/icon.png', ],
    'data': [
        'data/data.xml',
        'static/src/xml/assets.xml',
        'views/acquirer.xml',
        'views/templates.xml',
    ],
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
