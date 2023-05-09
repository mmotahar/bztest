from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        if self.sale_order_template_id:
            project_id = False
            sale_line_ids = []
            for rec in self.order_line:
                if rec.product_id.service_tracking == 'no':
                    if rec.product_id.matter_employee_id:
                        sale_line_ids.append((0, 0, {'employee_id':rec.product_id.matter_employee_id.id , 'sale_line_id': rec.id}))
                if rec.project_id:
                    project_id = rec.project_id
            project_id.sale_line_employee_ids = sale_line_ids
        return res

# class ProjectProductEmployeeMap(models.Model):
#     _inherit = 'project.sale.line.employee.map'
#
#     _sql_constraints = [
#         ('uniqueness_employee', 'CHECK(1=1)', 'An employee cannot be selected more than once in the mapping. Please remove duplicate(s) and try again.'),
#     ]
