from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    gst_grids_r = fields.Char(string="GST Grids", compute="_set_vals_in_gst_report", store=True)
    gst_sub_grids_r = fields.Char(string="GST Sub-Grids", compute="_set_vals_in_gst_report", store=True)
    gst_rpt_gross = fields.Monetary(compute="_gst_rpt_gross", string="Gross", store=True,
                                    currency_field='company_currency_id')
    gst_rpt_gst = fields.Monetary(compute="_gst_rpt_gst", string="GST", store=True,
                                  currency_field='company_currency_id')
    gst_rpt_net = fields.Monetary(compute="_gst_rpt_net", string="Net", store=True,
                                  currency_field='company_currency_id')
    x_studio_tax_code = fields.Many2one('account.tax', string="Tax Code", compute="_cal_tax_code", store=True)

    # order_by_fld = fields.Float(string="Custom Order By", default=-1)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        s_orderby = self._context.get('d_order', False)
        if s_orderby:
            # domain = domain + [('tax_tag_ids', '!=', False)
            domain = domain + [('move_id.state', '=', 'posted'),
                               ('x_studio_tax_code', '!=', False),
                               ('gst_grids_r', '!=', ""), ('gst_sub_grids_r', '!=', "")]
        result = super(AccountMoveLine, self).read_group(domain=domain, fields=fields, groupby=groupby, offset=offset,
                                                         limit=limit,
                                                         orderby=orderby, lazy=lazy)
        return result

    @api.depends('tax_ids', 'tax_line_id')
    def _cal_tax_code(self):
        for record in self:
            record.x_studio_tax_code = (record.tax_ids and record.tax_ids[0].id) or (
                    record.tax_line_id and record.tax_line_id[0].id)

    @api.depends('x_studio_tax_code', 'gst_rpt_gross')
    def _gst_rpt_net(self):
        for record in self:
            record.gst_rpt_net = record.gst_rpt_gross
            if (record.x_studio_tax_code.type_tax_use == 'sale' and record.x_studio_tax_code.amount > 0) or (
                    record.x_studio_tax_code.type_tax_use == 'purchase' and record.x_studio_tax_code.amount > 0) or record.account_id.name == 'GST Paid':
                record.gst_rpt_net = record.gst_rpt_gross - record.gst_rpt_gst

    @api.depends('x_studio_tax_code', 'gst_rpt_gross')
    def _gst_rpt_gst(self):
        for record in self:
            record.gst_rpt_gst = 0.00
            if not record.x_studio_tax_code.invoice_repartition_line_ids.filtered(
                    lambda x: x.repartition_type == 'tax' and x.tag_ids):
                record.gst_rpt_gst = 0.00
            elif (record.x_studio_tax_code.type_tax_use == 'sale' and record.x_studio_tax_code.amount > 0) or (
                    record.x_studio_tax_code.type_tax_use == 'purchase' and record.x_studio_tax_code.amount > 0):
                record.gst_rpt_gst = record.gst_rpt_gross / 11
            if record.account_id.name == 'GST Paid' and record.x_studio_tax_code and 'gst only' in record.x_studio_tax_code.name[
                                                                                                   :8].lower():
                record.gst_rpt_gst = record.gst_rpt_gross
            if record.x_studio_tax_code.amount > 1000 and record.x_studio_tax_code.invoice_repartition_line_ids.filtered(
                    lambda x: x.repartition_type == 'tax' and x.tag_ids and (
                            ('+ONLY' in x.tag_ids.mapped('name')) or ('ONLY' in x.tag_ids.mapped('name')) or (
                            'only' in x.tag_ids.mapped('name')))):
                record.gst_rpt_gst = record.gst_rpt_gross

    @api.depends('balance', 'x_studio_tax_code')
    def _gst_rpt_gross(self):
        for record in self:
            if record.x_studio_tax_code.type_tax_use == 'sale':
                record['gst_rpt_gross'] = -record.balance
            else:
                record['gst_rpt_gross'] = record.balance

    @api.depends('tax_tag_ids', 'x_studio_tax_code', 'move_id.state')
    def _set_vals_in_gst_report(self):
        for aml in self:
            aml.gst_grids_r = aml.gst_sub_grids_r = ""
            if aml.move_id.state == 'posted' and aml.tax_tag_ids:
                for tag in aml.tax_tag_ids.filtered(lambda x: 'GST from General Ledger' not in x.name):
                    tag_name = tag.name.replace('-', '').replace('+', '')
                    set_tag_name = tag.tax_report_line_ids.filtered(lambda x: x.code == tag_name) and \
                                   tag.tax_report_line_ids.filtered(lambda x: x.code == tag_name)[0].name
                    if tag_name in ['G10', 'G11', 'G17', 'G18']:
                        aml.gst_grids_r = "G12: Total Purchases (Including any GST)"
                        aml.gst_sub_grids_r = "G19: Total Purchases Subject to GST"
                    if tag_name in ['G19', 'G14']:
                        aml.gst_grids_r = "G12: Total Purchases (Including any GST)"
                        aml.gst_sub_grids_r = set_tag_name
                    if tag_name in ['ONLY']:
                        aml.gst_grids_r = "GST Only Purchases (GST On Imports)"
                        aml.gst_sub_grids_r = set_tag_name
                    if not aml.gst_grids_r and (
                            tag.tax_report_line_ids.filtered(lambda x: x.children_line_ids) or tag_name in ['G10',
                                                                                                            'G11',
                                                                                                            'G13',
                                                                                                            'G14',
                                                                                                            'G15',
                                                                                                            'G18']):
                        aml.gst_grids_r = set_tag_name
                    elif not aml.gst_sub_grids_r and tag_name not in ['G1', 'G10', 'G11']:
                        aml.gst_sub_grids_r = set_tag_name
                if ('G1:' in aml.gst_grids_r) and not aml.gst_sub_grids_r:
                    aml.gst_sub_grids_r = "Total Sales Subject to GST"
            if not aml.gst_sub_grids_r and not aml.gst_grids_r and aml.x_studio_tax_code and (
                    'BAS Excluded' in aml.x_studio_tax_code.name):
                aml.gst_grids_r = "BAS Excluded"
                aml.gst_sub_grids_r = "BAS Excluded"
            if not aml.gst_sub_grids_r and not aml.gst_grids_r and aml.x_studio_tax_code and (
                    'BAS Excluded (S)' in aml.x_studio_tax_code.name):
                aml.gst_grids_r = "BAS Excluded (S)"
                aml.gst_sub_grids_r = "BAS Excluded (S)"
            if not aml.gst_sub_grids_r and not aml.gst_grids_r and aml.x_studio_tax_code and (
                    'BAS Excluded (P)' in aml.x_studio_tax_code.name):
                aml.gst_grids_r = "BAS Excluded (P)"
                aml.gst_sub_grids_r = "BAS Excluded (P)"
            # aml.order_by_fld = 0
            # if 'G1: ' in aml.gst_grids_r[:4]:
            #     aml.order_by_fld = 100000000
            # elif 'G12:' in aml.gst_grids_r[:4]:
            #     aml.order_by_fld = 10000
            # elif 'GST O' in aml.gst_grids_r[:5]:
            #     aml.order_by_fld = 1