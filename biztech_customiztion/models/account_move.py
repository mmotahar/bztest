from odoo import api,  fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    login_user_id = fields.Many2one(comodel_name="res.users", string="Login User")
    custom_access_token = fields.Char(string="Custom Access Token", compute='get_custom_access_token')

    def get_custom_access_token(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param("web.base.url")
            payment_link_wizard = str(web_base_url) + '/my/invoices/' + str(rec.id) + '?access_token=' + str(
                rec.access_token)
            rec.custom_access_token = payment_link_wizard


    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
            'account.email_template_edi_credit_note'
            if all(move.move_type == 'out_refund' for move in self)
            else 'biztech_customiztion.account_move_tax_temp'
        )

    def action_invoice_print(self):
        return self.env.ref('biztech_invoice_reports.report_tax_invoice').report_action(self)


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    @api.onchange('template_id')
    def onchange_template_id(self):
        super().onchange_template_id()
        account_move = self.env['account.move'].browse(self.env.context.get('active_id'))
        account_move.login_user_id = self.env.user.id