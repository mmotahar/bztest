from odoo import api,  fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_process = fields.Selection(string='Payment Method', selection=[('Pre-Paid', 'Pre-Paid'), ('Post-Paid', 'Post-Paid')], default='Post-Paid')

    @api.onchange('payment_process')
    def onchange_payment_process(self):
        if self.payment_process == 'Pre-Paid':
            self.require_payment = True
        else:
            self.require_payment = False

    def action_quotation_send(self):
        if not self.payment_process:
            raise UserError("Kindly add Payment Method First!!")
        return super(SaleOrder, self).action_quotation_send()

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data']._xmlid_to_res_id('sale.mail_template_sale_confirmation',
                                                                         raise_if_not_found=False)
        if not template_id:
            default_email_temp = self.env['ir.config_parameter'].sudo().get_param('email_temp_id')
            template_id = int(default_email_temp)
        return template_id

