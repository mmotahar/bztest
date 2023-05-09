from odoo import api,  fields, models


class MatterType(models.Model):
    _name = 'matter.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Matter Type'

    name = fields.Char(string="Name")