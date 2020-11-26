# -*- coding: utf-8 -*-

from odoo import fields, models, _, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_commissioned = fields.Boolean('Works on commission?', default=True)
    comm_percent = fields.Float('Commission percentage')


class HrContract(models.Model):
    _inherit = 'hr.contract'

    comm = fields.Float('Pending Commission', default=0.0)
    is_commissioned = fields.Boolean('Works on commission?', related='employee_id.is_commissioned')

    @api.multi
    def calculate_commissions_amount(self, emp):
        comm_input = self.env['hr.salary.rule.input'].search(
            [('employee_id', '=', emp.id), ('state', '=', 'draft')], limit=1)
        return comm_input.total
