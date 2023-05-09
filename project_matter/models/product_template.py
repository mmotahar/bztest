from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    matter_employee_id = fields.Many2one(comodel_name="hr.employee",string="Matter Employee")