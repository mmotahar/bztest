# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger()

from odoo.addons.account.controllers.terms import TermsController

@http.route('/terms', type='http', auth='public', website=True, sitemap=True)
def terms_conditions(self, **kwargs):
    _logger.info("Called Terms And Condition URL")
    use_invoice_terms = request.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms')
    if not (use_invoice_terms and request.env.company.sudo().terms_type == 'html'):
        return request.render('http_routing.http_error', {
            'status_code': _('Oops'),
            'status_message': _("""The requested page is invalid, or doesn't exist anymore.""")})
    values = {
        'use_invoice_terms': use_invoice_terms,
        'company': request.env.company
    }
    return request.render("account.account_terms_conditions_page", values)

TermsController.terms_conditions = terms_conditions



