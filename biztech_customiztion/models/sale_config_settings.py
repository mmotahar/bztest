# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	email_temp_id = fields.Many2one(comodel_name="mail.template", string="Email Template", domain="[('model', '=', 'sale.order')]")
	show_preview_mail_temp_ids = fields.Many2many(comodel_name="mail.template", string="Email Template", domain="[('model', '=', 'sale.order')]")

	def set_values(self):
		self.env['ir.config_parameter'].sudo().set_param('email_temp_id', self.email_temp_id.id)
		self.env['ir.config_parameter'].sudo().set_param('show_preview_mail_temp_ids', self.show_preview_mail_temp_ids.ids)
		super(ResConfigSettings, self).set_values()

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		config_parameter = self.env['ir.config_parameter'].sudo()
		email_temp_id = config_parameter.get_param('email_temp_id')
		show_preview_mail_temp_ids = config_parameter.get_param('show_preview_mail_temp_ids')
		res.update(
			email_temp_id=int(email_temp_id),
			show_preview_mail_temp_ids=[(6, 0, literal_eval(show_preview_mail_temp_ids))] if show_preview_mail_temp_ids else False,
		)
		return res
