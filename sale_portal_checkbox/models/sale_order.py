from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    portal_checkbox = fields.Boolean(string='Show on Quote')
