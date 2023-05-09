from odoo import api,  fields, models,_
import re
from odoo.addons.mail.models.mail_thread import MailThread

@api.model
def message_new(self, msg_dict, custom_values=None):
    """Called by ``message_process`` when a new message is received
       for a given thread model, if the message did not belong to
       an existing thread.
       The default behavior is to create a new record of the corresponding
       model (based on some very basic info extracted from the message).
       Additional behavior may be implemented by overriding this method.

       :param dict msg_dict: a map containing the email details and
                             attachments. See ``message_process`` and
                            ``mail.message.parse`` for details.
       :param dict custom_values: optional dictionary of additional
                                  field values to pass to create()
                                  when creating the new thread record.
                                  Be careful, these values may override
                                  any other values coming from the message.
       :rtype: int
       :return: the id of the newly created thread object
    """
    data = {}
    if isinstance(custom_values, dict):
        data = custom_values.copy()
    fields = self.fields_get()
    name_field = self._rec_name or 'name'
    if name_field in fields and not data.get('name'):
        data[name_field] = msg_dict.get('subject', '')
    if 'Biztech Lawyers - Website Form' in msg_dict.get('subject') and self._name == 'crm.lead':
        return self.create(data)
    elif self._name != 'crm.lead':
        return self.create(data)

MailThread.message_new = message_new