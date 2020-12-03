# -*- coding: utf-8 -*-
import json
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class KushkiController(http.Controller):
    _return_url = '/payment/kushki/return/'
    _accept_url = '/payment/kushki/feedback'

    @http.route(['/payment/kushki/s2s/create'], type='http', auth='public', csrf=False)
    def kushki_s2s_create(self, **post):
        _logger.info('Beginning Kushki Cajita controller kushki_s2s_create with post data %s', pprint.pformat(post))
        acquirer_id = int(post.get('acquirer_id'))
        acquirer = request.env['payment.acquirer'].browse(acquirer_id)
        acquirer.s2s_process(post)
        return werkzeug.utils.redirect(post.get('return_url', '/'))



