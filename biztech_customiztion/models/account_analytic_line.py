from odoo import api,  fields, models
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    billable = fields.Float(string="Billable", compute="get_total_rate")
    # billable_1 = fields.Float(string="Billable", help="Use for group by")
    billable_2 = fields.Float(string="Billable", help="Use for group by", compute='compute_billable_2', store=True)

    def calculate_billable_amt_for_existing(self):
        existing_recs = self.env['account.analytic.line'].search([])
        for rec in existing_recs:
            rec.get_total_rate_2()

    # @api.onchange('unit_amount', 'x_studio_rate', 'project_id', 'task_id', 'employee_id')
    # def get_total_billable_2(self):
    #     print(9999999999999999999999999999999999999999, self.x_studio_rate, self.unit_amount)
    #     self.billable = 0.0
    #     if self.x_studio_rate and self.unit_amount:
    #         hours = self.unit_amount / 60
    #         # self.billable_2 = hours * (self.so_line.price_unit * 60)
    #         print(888888888888888888888888888, self.billable_2)
    #         self.update({
    #             'billable_2': hours * (self.so_line.price_unit * 60)
    #         })

    @api.depends('unit_amount', 'x_studio_rate', 'project_id', 'task_id', 'employee_id')
    def compute_billable_2(self):
        for rec in self:
            rec.billable_2 = 0.0
            if rec.x_studio_rate and rec.unit_amount:
                hours = rec.unit_amount/60
                rec.billable_2 = hours * (rec.so_line.price_unit*60)
    def get_total_rate(self):
        for rec in self:
            rec.billable = 0.0
            if rec.x_studio_rate and rec.unit_amount:
                hours = rec.unit_amount/60
                rec.billable = hours * (rec.so_line.price_unit*60)


class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    expense_manager_id = fields.Many2one('res.users', readonly=True)