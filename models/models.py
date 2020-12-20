# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Cus_nuboogh(models.Model):
    _inherit="account.move"
    warehouse_location_id = fields.Many2one('stock.picking',compute='calc_warehouse_location_id')
    total_qty = fields.Integer(compute="count_sold_item")  
    invoice_type = fields.Selection([('monetory', 'نقدي'), ('temem','ذمم')] , string="نوع الفاتورة" , default="temem")
    previous_customer_debit = fields.Monetary(compute="_get_prev_debit")

    @api.onchange("partner_id")
    def _get_prev_debit(self):
        if self.partner_id:
            invoice_payed_amount = self.amount_total - self.amount_residual
            self.previous_customer_debit = self.partner_id.total_due + invoice_payed_amount
        else:
            self.previous_customer_debit = False


    @api.depends("partner_id")
    def calc_warehouse_location_id(self):
        if self.invoice_origin:
            transfers=self.env["stock.picking"].search([("origin","=",self.invoice_origin)], limit=1)
            if transfers:
                self.warehouse_location_id = transfers.id
            else:
                self.warehouse_location_id = False
        else:
            self.warehouse_location_id = False

    @api.depends("invoice_line_ids")
    def count_sold_item(self):
        total_qty = 0
        for line in self.invoice_line_ids:
            total_qty += line.quantity
        self.total_qty = total_qty


class ProductTemplateExt(models.Model):
    _inherit = 'product.template'
    product_type = fields.Char(string="الموديل")
    country_of_origin = fields.Char(string="بلد المنشأ")        
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج")
    name_en = fields.Char(string=" اسم المادة بالانكليزي")

# class UserExt(models.Model):
#     _inherit = 'res.users'
#     sales_person = fields.Many2one('res.partner')
