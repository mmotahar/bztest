
from odoo import models, fields, api
from datetime import date


class FinalInvoiceReport(models.AbstractModel):
    _name = 'report.account.report_invoice_with_payments_copy_1_copy_1'
    _description = 'Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['account.move'].browse(docids)

        def get_employee_initial(timesheet):
            if timesheet.employee_id:
                initial_str = ''
                for li in timesheet.employee_id.name.split():
                    initial_str += li[0]
                return initial_str

        def get_timesheet_in_order(timesheet_ids):
            return timesheet_ids.sorted('date')

        def get_project_name(o):
            if o.invoice_origin:
                invoice_id_li = []
                invoice_id_li.append(o.id)
                if invoice_id_li:
                    so_project_name = self.env['sale.order'].search([('invoice_ids', 'in', invoice_id_li)], limit=1)
                    return so_project_name

        def get_outstanding_balance(o):
            if o.state == 'posted':
                outstanding_balance = o.partner_id.total_due - o.amount_total
            else:
                outstanding_balance = o.partner_id.total_due
            if outstanding_balance < 1:
                outstanding_balance = 0
            return outstanding_balance

        def get_payments(o):
            payments = self.env['account.payment'].search([])
            for pay in payments:
                payment_amt = 0
                for recon in pay.reconciled_invoice_ids:
                    if recon.id == o.id:
                        payment_amt += pay.amount
                return payment_amt

        def get_tax_totals(tax_totals):
            tax_amt_total = 0
            for tax in tax_totals:
                tax_amt_total += tax['tax_group_amount']
            return tax_amt_total

        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'get_employee_initial': get_employee_initial,
            'get_timesheet_in_order': get_timesheet_in_order,
            'get_project_name': get_project_name,
            'get_outstanding_balance': get_outstanding_balance,
            'get_payments': get_payments,
            'get_tax_totals': get_tax_totals,
        }