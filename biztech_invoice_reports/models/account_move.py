from odoo import api,  fields, models
from datetime import datetime, timedelta

class AccountMoveExt(models.Model):
    _inherit = 'account.move'

    is_display_discounts_in_invoice = fields.Boolean(string="Display Discounts in Invoice", default=False)
    due_days = fields.Char(compute="compute_calculate_days")


    def compute_calculate_days(self):
        for move in self:
            if move.invoice_date_due and move.invoice_date:
                difference = move.invoice_date_due - move.invoice_date
                move.due_days = difference.days
            else:
                move.due_days = 0
    