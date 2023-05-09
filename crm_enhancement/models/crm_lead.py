from odoo import api,  fields, models,_
import re
from odoo.addons.crm.models.crm_lead import Lead
from odoo.addons.crm.models import crm_stage
import logging
_logger = logging.getLogger(__name__)

@api.model
def message_new(self, msg_dict, custom_values=None):
    """ Overrides mail_thread message_new that is called by the mailgateway
        through message_process.
        This override updates the document according to the email.
    """
    # remove default author when going through the mail gateway. Indeed we
    # do not want to explicitly set an user as responsible. We prefer that
    # assignment is done automatically (scoring) or manually. Otherwise it
    # would always be either root (gateway user) either alias owner (through
    # alias_user_id). It also allows to exclude portal / public users.
    self = self.with_context(default_user_id=False)

    if custom_values is None:
        custom_values = {}
    msg = msg_dict.get('body')

    email_from = msg[msg.find('&lt;') + 4:]
    _logger.info("Email From Body : {0}".format(email_from))
    email_from_data = []
    for e in email_from:
        if e == '&':
            break
        email_from_data.append(str(e))
    email_from = ''.join(email_from_data)
    _logger.info("Final From Email: {0}".format(email_from))
    phone = msg[msg.find('Phone:') + 7:]
    _logger.info("Phone From Body: {0}".format(phone))
    phone_data = []
    for p in phone:
        if p == '\r':
            break
        phone_data.append(str(p))
    phone = ''.join(phone_data)
    _logger.info("Final From Phone: {0}".format(phone))
    message = msg[msg.find('Message Body:') + 15:]
    _logger.info("Message From Body: {0}".format(message))
    message_data = []
    for m in message:
        if m == '<':
            break
        message_data.append(str(m))
    message = ''.join(message_data)
    _logger.info("Final From Message: {0}".format(message))
    contact_name = msg[msg.find('From:') + 6:]
    name_data = []
    for c in contact_name:
        if c == '&':
            break
        name_data.append(str(c))
    contact_name = ''.join(name_data)
    _logger.info("Final From Contact Name: {0}".format(contact_name))
    defaults = {
        'name':  msg_dict.get('subject') or _("No Subject"),
        'email_from': email_from or msg_dict.get('from'),
        'partner_id': msg_dict.get('author_id', False),
        'phone':phone,
        'description':message,
        'contact_name':contact_name
    }
    if msg_dict.get('priority') in dict(crm_stage.AVAILABLE_PRIORITIES):
        defaults['priority'] = msg_dict.get('priority')
    defaults.update(custom_values)

    # assign right company
    if 'company_id' not in defaults and 'team_id' in defaults:
        defaults['company_id'] = self.env['crm.team'].browse(defaults['team_id']).company_id.id
    return super(Lead, self).message_new(msg_dict, custom_values=defaults)

Lead.message_new = message_new

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Individual'), ('company', 'Company')])
    matter_type_ids = fields.Many2many(comodel_name="matter.type", string="Matter Type")
    main_concern_ids = fields.Many2many(comodel_name="main.concern", string="Main Concern")
    product_ids = fields.Many2many(comodel_name="product.template", string="Product")
    pipeline_company_id = fields.Many2one(comodel_name="res.company", string="Pipeline Company")
    date_of_birth = fields.Date(string="Date of Birth ", tracking=True)
    website = fields.Char(string="Website", tracking=True)
    opportunity_description = fields.Char(string="Description", tracking=True)
    company_short_name = fields.Char(string="Company Short Name", tracking=True)

    @api.onchange('partner_id', 'opportunity_description')
    def onchange_client_description(self):
        if self.partner_id and self.opportunity_description:
            self.name = self.partner_id.name+'-'+self.opportunity_description
        elif not self.opportunity_description and self.partner_id:
            self.name = self.partner_id.name
        elif self.opportunity_description and not self.partner_id:
            self.name = self.opportunity_description

    @api.onchange('website')
    def onchange_website(self):
        if self.website:
            self.company_short_name = self.website.split("www.")[-1].split("//")[-1].split(".")[0]

    def action_new_quotation(self):
        res = super(CrmLead, self).action_new_quotation()
        res['context'].update({'default_x_studio_matter': self.opportunity_description})
        return res

    def write(self, values):
        print(777777777777777777777777777, values)
        contact = self.env['res.partner'].search([('email', '=', self.email_from)], limit=1)
        contact_dict = {}
        if values.get('contact_name'):
            contact_dict.update({'name': values.get('contact_name')})
        if values.get('email_from'):
            contact_dict.update({'email': values.get('email_from')})
        if values.get('function'):
            contact_dict.update({'function': values.get('function')})
        if values.get('phone'):
            contact_dict.update({'phone': values.get('phone')})
        if values.get('mobile'):
            contact_dict.update({'mobile': values.get('mobile')})
        if values.get('company_short_name'):
            contact_dict.update({'x_studio_company_short_name': values.get('company_short_name')})
        if values.get('website'):
            contact_dict.update({'website': values.get('website')})
        if values.get('date_of_birth'):
            contact_dict.update({'date_of_birth': values.get('date_of_birth')})
        if values.get('x_studio_gendar_1'):
            contact_dict.update({'x_studio_gendar': values.get('x_studio_gendar_1')})
        if values.get('x_studio_license'):
            contact_dict.update({'x_studio_license': values.get('x_studio_license')})
        if values.get('x_studio_tax_id'):
            contact_dict.update({'vat': values.get('x_studio_tax_id')})
        if values.get('street'):
            contact_dict.update({'street': values.get('street')})
        if values.get('street2'):
            contact_dict.update({'street2': values.get('street2')})
        if values.get('city'):
            contact_dict.update({'city': values.get('city')})
        if values.get('state_id'):
            contact_dict.update({'state_id': values.get('state_id')})
        if values.get('zip'):
            contact_dict.update({'zip': values.get('zip')})
        if values.get('country_id'):
            contact_dict.update({'country_id': values.get('country_id')})
        contact.update(contact_dict)
        # For Update Sale order field
        # if values.get('opportunity_description'):
        #     if self.order_ids:
        #         for order in self.order_ids:
        #             order.update({'x_studio_matter': values.get('opportunity_description', False)})

        return super(CrmLead, self).write(values)


