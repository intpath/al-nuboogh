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
            self.previous_customer_debit = self.partner_id.total_due - self.amount_total
        else:
            self.previous_customer_debit = False


    @api.depends("partner_id")
    def calc_warehouse_location_id(self):
        if self.invoice_origin:
            transfers=self.env["stock.picking"].search([("origin","=",self.invoice_origin)], order="id desc", limit=1)
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

class AccountPyament(models.Model):
    _inherit = "account.payment"
    partner_due = fields.Monetary(string="مستحق الزبون/المجهز" ,related="partner_id.total_due")
    partner_id = fields.Many2one("res.partner", domain="[('company_id', 'in', [company_id, False])]")
    
class ProductTemplateExt(models.Model):
    _inherit = 'product.template'
    product_type = fields.Char(string="الموديل")
    product_type_en = fields.Char(string="الموديل بالإنكليزي")
    country_of_origin = fields.Char(string="بلد المنشأ")        
    country_of_origin_en = fields.Char(string="بلد المنشأ بالإنكليزي")        
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج")
    name_en = fields.Char(string=" اسم المادة بالانكليزي")

    
class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    product_model_type = fields.Char(string="الموديل", related="product_id.product_type")
    product_country_of_origin = fields.Char(string="بلد المنشأ", related="product_id.country_of_origin")        
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج", related="product_id.product_name_2")

    
class PurchaseOrder(models.Model):
    _inherit="purchase.order.line"
    product_type_en = fields.Char(string="الموديل بالإنكليزي", related="product_id.product_type_en")
    product_country_of_origin_en = fields.Char(string="بلد المنشأ بالإنكليزي", related="product_id.country_of_origin_en") 
    product_name_en = fields.Char(string=" اسم المادة بالانكليزي", related="product_id.name_en")



class  ProductProductext(models.Model):
    _inherit="product.product"

    display_name = fields.Char(compute="_compute_full_names")

    def _compute_full_names(self):
        for item in self:
            # raise UserError( str(item.product_name_2) ) 
            if item.product_name_2:
                item.display_name = item.name + " - " + item.product_name_2
            else:
                item.display_name = item.name

#    @api.model
    def name_get(self):
        result = []
        for record in self:
                    result.append((record.id, record.display_name))
        return result
