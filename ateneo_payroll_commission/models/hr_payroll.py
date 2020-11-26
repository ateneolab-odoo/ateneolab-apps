# -*- coding: utf-8 -*-
# AteneoLab Ltda.
########################################

from odoo import fields, models, _, api
from odoo.exceptions import UserError
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta


class HrInput(models.Model):
    _name = 'hr.salary.rule.input'
    _description = 'Salary Rule Input'

    name = fields.Char('Name', readonly=True,
                       states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True,
                                  states={'draft': [('readonly', False)]})
    category_id = fields.Many2one('hr.salary.rule.category', 'Category', readonly=True,
                                  states={'draft': [('readonly', False)]})
    amount = fields.Float('Amount', readonly=True,
                          states={'draft': [('readonly', False)]})
    amount_untaxed = fields.Float('Amount untaxed', readonly=True,
                                  states={'draft': [('readonly', False)]})
    total = fields.Float('Total', readonly=True,
                         states={'draft': [('readonly', False)]})
    commission_id = fields.Many2one('hr.commission', 'Commission Salary Rules', readonly=True,
                                    states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('cancelled', 'Cancelled')], 'State', default='draft')

    @api.multi
    def unlink(self):
        raise UserError(_('You can not delete record.'))


class HrCommission(models.Model):
    _name = 'hr.commission'
    _description = 'Commissions'

    name = fields.Char('Name', store=True,
                       default=_('Commissions - ' + datetime.now().strftime('%B').upper()))
    date_generated = fields.Datetime('Date generated', default=datetime.now().strftime(DF), readonly=True,
                                     states={'draft': [('readonly', False)]})
    date_init = fields.Date('Date init', readonly=True,
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            states={'draft': [('readonly', False)]})
    date_end = fields.Date('Date end', readonly=True, default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
                           states={'draft': [('readonly', False)]})
    salary_ids = fields.One2many('hr.salary.rule.input', 'commission_id', 'Salary Rules', readonly=True,
                                 states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('processed', 'Processed'),
        ('cancelled', 'Cancelled')], 'State', default='draft')

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         u'You already have generated commissions for this period!')]

    def set_cancelled(self):
        self.salary_ids.write({'state': 'cancelled'})
        return self.write({'state': 'cancelled'})

    @api.model
    def get_contract(self, employee, date_from, date_to):
        clause_1 = ['&', ('date_end', '<=', date_to), ('date_end', '>=', date_from)]
        # OR if it starts between the given dates
        clause_2 = ['&', ('date_start', '<=', date_to), ('date_start', '>=', date_from)]
        # OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&', ('date_start', '<=', date_from), '|', ('date_end', '=', False), ('date_end', '>=', date_to)]
        clause_final = [('employee_id', '=', employee.id), ('state', '=', 'open'), '|',
                        '|'] + clause_1 + clause_2 + clause_3
        return self.env['hr.contract'].search(clause_final).ids

    @api.multi
    def generate_inputs_commission(self):
        for record in self:
            salary_input_obj = self.env['hr.salary.rule.input']
            invoices_obj = self.env['account.invoice']
            all_list = self.env['hr.employee'].search([('is_commissioned', '=', True)])
            active_list = []
            invoicing_data = []
            for emp in all_list:
                contract_by_emp = record.get_contract(emp, record.date_init, record.date_end)
                if len(contract_by_emp) > 0:
                    active_list.append(emp)
            for act in active_list:
                sum_inv = 0
                sum_untaxed_inv = 0
                for inv in invoices_obj.search(
                        [('user_id', '=', act.user_id.id), ('date_invoice', '<=', record.date_end),
                         ('date_invoice', '>=', record.date_init)]).filtered(
                            lambda x: x.state in ['open', 'in_payment', 'paid']):
                    sum_inv += inv.amount_total
                    sum_untaxed_inv += inv.amount_untaxed
                if sum_inv > 0:
                    invoicing_data.append(
                        {
                            'employee_id': act.id,
                            'amount_total': sum_inv,
                            'amount_untaxed': sum_untaxed_inv,
                            'total': float(sum_inv * act.comm_percent / 100),
                        })
            if invoicing_data:
                for invo in invoicing_data:
                    salary_input_obj.create(
                        {
                            'name': record.name,
                            'employee_id': invo['employee_id'],
                            'category_id': self.env.ref('hr_payroll.ALW').id,
                            'amount': invo['amount_total'],
                            'amount_untaxed': invo['amount_untaxed'],
                            'total': invo['total'],
                            'state': 'draft',
                            'commission_id': record.id,
                        })
                    record.env['hr.contract'].search([('employee_id', '=', invo['employee_id'])], limit=1).write(
                        {'comm': invo['total']})
            else:
                raise UserError('There are no invoiced values for this period, '
                                'so no commission inputs can be generated for current payroll.')
            super(HrCommission, record).write({'state': 'generated'})
        return True

    @api.multi
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('You can only delete records in Draft state.'))
            else:
                super(HrCommission, self).unlink()


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        com = False
        for payslip in self:
            contract = payslip.contract_id
            for line in payslip.line_ids:
                if line.code == 'CMM':
                    com = True
                    pass
            if com:
                contract.write({'comm': 0.0})
                flag = False
                comm = self.env['hr.commission'].search([('state', '=', 'generated')], limit=1)
                for rec in comm.salary_ids:
                    if rec.employee_id == payslip.employee_id:
                        rec.write({'state': 'processed'})
                    if rec.state != 'processed':
                        flag = True
                if not flag:
                    comm.write({'state': 'processed'})
        return res
