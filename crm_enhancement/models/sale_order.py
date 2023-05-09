from odoo import api,  fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    seq_number = fields.Char(string="Sequence Number")

    def update_sequence_for_existing_so(self):
        so_recs = self.env['sale.order'].search([])
        for so in so_recs:
            so.seq_number = so.name[1:7]

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        res.seq_number = res.name[1:]
        sequence = 'Q '+res.name[1:]
        if res.partner_id and res.x_studio_matter:
            if res.partner_id.parent_id:
                sequence += '-'+res.partner_id.parent_id.name+'-'+res.x_studio_matter
            else:
                sequence += '-' + res.partner_id.name + '-' + res.x_studio_matter
        elif res.partner_id and not res.x_studio_matter:
            if res.partner_id.parent_id:
                sequence += '-'+res.partner_id.parent_id.name
            else:
                sequence += '-' + res.partner_id.name
        if not res.partner_id and res.x_studio_matter:
            sequence += '-'+res.x_studio_matter
        res.update({
            'name': sequence
        })
        return res

    def write(self, values):
        if values.get('x_studio_matter') or values.get('partner_id'):
            if values.get('x_studio_matter'):
                if self.opportunity_id:
                    self.opportunity_id.opportunity_description = values.get('x_studio_matter')
                    self.opportunity_id.onchange_client_description()
            if values.get('partner_id') and values.get('x_studio_matter'):
                partner = self.env['res.partner'].browse(values.get('partner_id'))
                matter_desc = values.get('x_studio_matter')
                if partner.parent_id:
                    sequence = 'Q ' + self.seq_number + '-' + partner.parent_id.name+'-'+matter_desc
                else:
                    sequence = 'Q ' + self.seq_number + '-' + partner.name + '-' + matter_desc
                self.update({
                    'name': sequence
                })
                if self.project_ids:
                    for project in self.project_ids:
                        project.name = self.name[2:]
            elif not values.get('x_studio_matter') and values.get('partner_id'):
                partner = self.env['res.partner'].browse(values.get('partner_id'))
                if partner.parent_id:
                    sequence = 'Q ' + self.seq_number+'-'+partner.parent_id.name+'-'+self.x_studio_matter
                else:
                    sequence = 'Q ' + self.seq_number + '-' + partner.name + '-' + self.x_studio_matter
                self.update({
                    'name': sequence
                })
                if self.project_ids:
                    for project in self.project_ids:
                        project.name = self.name[2:]
            elif values.get('x_studio_matter') and not values.get('partner_id'):
                matter_desc = values.get('x_studio_matter')
                sequence = 'Q ' + self.seq_number + '-' + self.partner_id.name + '-' + matter_desc
                self.update({
                    'name': sequence
                })
                if self.project_ids:
                    for project in self.project_ids:
                        project.name = self.name[2:]
        return super(SaleOrder, self).write(values)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.name:
            for project in self.project_ids:
                tags = []
                project.name = self.name[2:]
                if self.tag_ids:
                    for tag in self.tag_ids:
                        tags.append(tag.name)
                project.x_studio_pratice_area = ','.join(tags)
        return res