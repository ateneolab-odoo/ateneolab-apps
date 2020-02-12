# -*- coding: utf-8 -*-
{
    "name": """POS discount authorization code""",
    "summary": """Provides authorization code for discounts in POS""",
    "category": "Point of Sale",
    "version": "10",
    "author": "AteneoLab",
    "support": "info@ateneolab.com",
    "website": "http://ateneolab.com",
    "license": "LGPL-3",
    "depends": [
        "pos_discount",
    ],
    'price': 0.00,
    "data": [
        "views/template.xml",
        'views/pos_config_view.xml',
    ],
    "qweb": ['static/src/xml/pos_code_view.xml'],
    'images': ['static/description/thumbnail.png',
                'static/description/banner_discount.png',
               'static/description/code_screen.png',
               'static/description/discount.png',
               'static/description/discount_settings.png',
               'static/description/icon.png',],
    "auto_install": False,
    "installable": True,
    "application": False,
}
