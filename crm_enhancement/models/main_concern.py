from odoo import api,  fields, models


class MainConcern(models.Model):
    _name = 'main.concern'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Main Concern'

    name = fields.Char(string="Name")