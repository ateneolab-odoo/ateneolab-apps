# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from odoo.exceptions import UserError
from numpy.core.defchararray import isdigit

class PosConfig(models.Model):
    _inherit = "pos.config"

    code = fields.Char('Authorized Code', size=4, help=u'Four digits code. It grants access to the POS salesman to apply discounts from POS UI.')

    @api.multi
    def write(self, vals):
        if vals.get('code', False) and not isdigit(vals.get('code', False)):
            raise UserError(u'Authorized code must be a 4 digits number.')
        res = super(PosConfig, self).write(vals)
        return res
