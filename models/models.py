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
    product_type_en = fields.Char(string="الموديل بالإنكليزي")
    country_of_origin = fields.Char(string="بلد المنشأ")        
    country_of_origin_en = fields.Char(string="بلد المنشأ بالإنكليزي")        
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج")
    name_en = fields.Char(string=" اسم المادة بالانكليزي")
    display_name = fields.Char(compute="_compute_display_name")

    

    
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

    full_name = fields.Char(compute="_compute_display_name")

    def _compute_display_name(self):
        for item in self:
            # raise UserError( str(item.product_name_2) ) 
            if item.product_name_2:
                item.full_name = item.name + " - " + item.product_name_2
            else:
                item.full_name = item.name

    @api.model
    def name_get(self):
        result = []
        for record in self:
                if record.full_name:
                    record_name = record.full_name
                    result.append((record.id, record_name))
                else:
                    record_name = record.name
                    result.append((record.id, record_name))
        return result