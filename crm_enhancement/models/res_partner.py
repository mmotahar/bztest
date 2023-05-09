from odoo import api,  fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Madura said remove default as a Newsletter
    # @api.model
    # def default_get(self, fields):
    #     res = super(ResPartner, self).default_get(fields)
    #     res_partner_category = self.env['res.partner.category'].search([('name','=', 'Newsletter Recipient')], limit=1)
    #     res['category_id'] = res_partner_category.ids
    #     return res

    date_of_birth = fields.Date(string="Date of Birth ", tracking=True)

    @api.onchange('website')
    def onchange_website(self):
        if self.website:
            self.x_studio_company_short_name = self.website.split("www.")[-1].split("//")[-1].split(".")[0]