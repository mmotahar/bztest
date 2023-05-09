from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    name = fields.Char("Name", index=True, required=True, tracking=True, translate=False)
    counterparty_id = fields.Many2one(comodel_name="res.partner", string="Counterparty")
    counterparty_email = fields.Char(string="Email", related="counterparty_id.email")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")