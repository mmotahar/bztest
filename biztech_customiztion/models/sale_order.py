from odoo import api,  fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_send_link = fields.Boolean(string="Link send in email template", default=False)
    login_user_id = fields.Many2one(comodel_name="res.users", string="Login User")
    custom_access_token = fields.Char(string="Custom Access Token", compute='get_custom_access_token')
    email_template_name = fields.Char(string="Template Name")

    # def get_custom_access_token(self):
    #     for rec in self:
    #         payment_link_wizard = (self.env["portal.share"].with_context(active_model="sale.order", active_id=rec.id).create({}))
    #         rec.custom_access_token = payment_link_wizard.share_link

    def get_custom_access_token(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param("web.base.url")
            payment_link_wizard = str(web_base_url)+'/my/orders/'+str(rec.id)+'?access_token='+str(rec.access_token)
            rec.custom_access_token = payment_link_wizard


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.onchange('template_id')
    def onchange_template_id(self):
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        show_preview_mail_temp_ids = self.env['ir.config_parameter'].sudo().get_param('show_preview_mail_temp_ids')
        if self.template_id.id in eval(show_preview_mail_temp_ids):
            sale_order.is_send_link = True
            sale_order.email_template_name = self.template_id.name
            sale_order.login_user_id = self.env.user.id
        else:
            sale_order.is_send_link = False
            sale_order.login_user_id = self.env.user.id

    def action_send_mail(self):
        res = super(MailComposeMessage, self).action_send_mail()
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        sale_order.email_template_name = ''
        return res

