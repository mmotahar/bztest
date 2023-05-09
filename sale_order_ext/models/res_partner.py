from odoo import api,  fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_filed_csn = fields.Boolean(string="Fill Company Short Name", default=False)

    @api.onchange('lastname')
    def onchange_lastname(self):
        self.x_studio_company_short_name = self.lastname

    def fill_company_short_name(self, limit=500):
        individuals = self.env['res.partner'].search([('company_type', '=', 'person'), ('is_filed_csn', '!=', True)], limit=limit)
        for individual in individuals:
            individual.x_studio_company_short_name = individual.lastname
