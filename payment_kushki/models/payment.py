# coding: utf-8
import json
import logging
import json
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

import requests


class AcquirerKushki(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('kushki', 'Kushki')],
                                ondelete={'kushki': 'set default'},
                                default="kushki")
    kushki_merchant_account = fields.Char('Llave pública',
                                          required_if_provider='kushki',
                                          groups='base.group_user')
    kushki_private_merchant_id = fields.Char('Llave privada',
                                             required_if_provider='kushki',
                                             groups='base.group_user')
    regional = fields.Boolean('Regional', groups='base.group_user',
                              help=u"Marcar si se usa una IP estática para acceder a Kushki",
                              default=False)

    def kushki_get_form_action_url(self):
        return '/payment/kushki/feedback'

    @api.model
    def _get_kushki_urls(self, environment):
        if environment == "test":
            return {'kushki_form_url': 'https://api-uat.kushkipagos.com', }
        else:
            return {'kushki_form_url': 'https://api.kushkipagos.com', }

    @api.model
    def _get_kushki_api_url(self):
        return self._get_kushki_urls(self.state)['kushki_form_url']

    def kushki_form_generate_values(self, tx_values):
        self.ensure_one()
        kushki_tx_values = dict(tx_values)
        temp_kushki_tx_values = {
            'company': self.company_id.name,
            'amount': tx_values['amount'],  # Mandatory
            'currency': tx_values['currency'].name,  # Mandatory anyway
            'currency_id': tx_values['currency'].id,  # same here
            'address_line1': tx_values.get('partner_address'),
            # Any info of the partner is not mandatory
            'address_city': tx_values.get('partner_city'),
            'address_country': tx_values.get(
                'partner_country') and tx_values.get(
                'partner_country').name or '',
            'email': tx_values.get('partner_email'),
            'address_zip': tx_values.get('partner_zip'),
            'name': tx_values.get('partner_name'),
            'phone': tx_values.get('partner_phone'),
        }

        temp_kushki_tx_values['returndata'] = kushki_tx_values.pop('return_url',
                                                                   '')
        temp_kushki_tx_values['regional'] = "true" if self.regional else "false"
        kushki_tx_values.update(temp_kushki_tx_values)
        return kushki_tx_values

    @api.model
    def kushki_s2s_form_process(self, values):
        if values.get('merchant_id') and values.get(
                'kushkiToken') and values.get('amount') and values.get(
                'currency'):
            payment_acquirer = self.env['payment.acquirer'].browse(
                int(values.get('acquirer_id')))
            api_url = payment_acquirer._get_kushki_api_url()
            url_charges = '%s/card/v1/charges' % api_url
            header_deferred = {'content-type': 'application/json',
                               'public-merchant-id': values.get(
                                   'merchant_id').encode('ascii'),
                               'private-merchant-id': values.get(
                                   'private_merchant_id').encode('ascii')}

            customer_params = {
                "token": values.get('kushkiToken'),
                "amount": {
                    "subtotalIva": 0,
                    "subtotalIva0": float(values.get('amount')),
                    "ice": 0,
                    "iva": 0,
                    "currency": values.get('currency')
                },
                "deferred": {
                    "graceMonths": "",
                    "creditType": "",
                    "months": ""
                },
                "metadata": {
                    "contractID": values.get('reference')
                },
                "fullResponse": True
            }
            if values.get('kushkiDeferred') and values.get(
                    'kushkiDeferredType'):
                customer_params["deferred"]["creditType"] = values.get(
                    'kushkiDeferredType')
                customer_params["deferred"]["months"] = values.get(
                    'kushkiDeferred')
                customer_params["deferred"]["graceMonths"] = values.get(
                    'kushkiDeferred')
            else:
                customer_params.pop("deferred", None)

            _logger.info(url_charges)
            _logger.info(header_deferred)
            _logger.info(json.dumps(customer_params))

            r = requests.post(url_charges, data=json.dumps(customer_params),
                              headers=header_deferred)
            if r.status_code in (200, 201,):
                charge = json.loads(r.text)
                _logger.info(charge)
                charge.update({"reference": values.get("reference")})
                self.env['payment.transaction'].sudo().form_feedback(charge,
                                                                     'kushki')
            else:
                # raise UserError(r.text)
                self.env['payment.transaction'].sudo().form_feedback(
                    {"reference": values.get("reference"),
                     "error_message": r.text}, 'kushki')
        else:
            _logger.info(
                'Faltan datos para ejucutar el cargo a la tarjeta datos provistos: %s' % str(
                    values))
        for field_name in ["cc_number", "cvc", "cc_holder_name", "cc_expiry",
                           "kushkiToken", "merchant_id", 'kushkiDeferredType',
                           'kushkiDeferred', 'reference', 'amount', 'currency']:
            values.pop(field_name, None)
        return None

    def kushki_s2s_form_validate(self, data):
        if data.get('message'):
            raise UserError("%s \n %s" % (
            charge.get('message', ""), charge.get('details', "")))
        return True


class PaymentTransactionKushki(models.Model):
    _inherit = 'payment.transaction'

    def _create_kushki_charge(self, acquirer_ref=None, tokenid=None,
                              email=None):
        api_url_charge = self.acquirer_id._get_kushki_api_url() + "/card/v1/charges"
        charge_params = {
            'amount': int(
                self.amount if self.currency_id.name in INT_CURRENCIES else float_round(
                    self.amount * 100, 2)),
            'currency': self.currency_id.name,
            'metadata[reference]': self.reference
        }
        if acquirer_ref:
            charge_params['customer'] = acquirer_ref
        if tokenid:
            charge_params['card'] = str(tokenid)
        if email:
            charge_params['receipt_email'] = email
        r = requests.post(api_url_charge, params=charge_params)
        return r.json()

    def _kushki_s2s_validate_tree(self, tree):
        self.ensure_one()
        if self.state != 'draft':
            _logger.info(
                'Kushki: trying to validate an already validated tx (ref %s)',
                self.reference)
            return True

        if tree.get("error_message"):
            _logger.warn(tree.get("error_message"))
            self.sudo().write({
                'state_message': tree.get("error_message"),
                'acquirer_reference': tree.get('id'),
                'date': fields.datetime.now(),
            })
            error = tree.get("error_message", "")
            self._set_transaction_error(error)
            return False

        status = tree.get("details", {}).get('transactionStatus')
        if status == 'APPROVAL':
            self.write({
                'date': fields.datetime.now(),
                'acquirer_reference': tree.get('ticketNumber'),
            })
            self._set_transaction_done()
            self.execute_callback()
            if self.payment_token_id:
                self.payment_token_id.verified = True
            return True
        else:
            error = tree.get('message', "")
            _logger.warn(error)
            self.sudo().write({
                'state_message': error,
                'acquirer_reference': tree.get('id'),
                'date': fields.datetime.now(),
            })
            self._set_transaction_cancel()
            return False

    def kushki_s2s_do_transaction(self, **kwargs):
        self.ensure_one()
        result = self._create_kushki_charge(
            acquirer_ref=self.payment_token_id.acquirer_ref,
            email=self.partner_email)
        return self._kushki_s2s_validate_tree(result)

    @api.model
    def _kushki_form_get_tx_from_data(self, data):
        """ Given a data dict coming from kushki, verify it and find the related
        transaction record. """
        reference = data.get('reference')
        if not reference:
            error_msg = _(
                'Kushki: invalid reply received from provider, missing reference. Additional message: %s'
                % data.get('error', {}).get('message', '')
            )
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        tx = self.search([('reference', '=', reference)])
        if not tx:
            error_msg = (_(
                'Kushki: no order found for reference %s') % reference)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        elif len(tx) > 1:
            error_msg = (_('Kushki: %s orders found for reference %s') % (
            len(tx), reference))
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def _kushki_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        reference = data['reference']
        if reference != self.reference:
            invalid_parameters.append(('Reference', reference, self.reference))
        return invalid_parameters

    def _kushki_form_validate(self, data):
        return self._kushki_s2s_validate_tree(data)
