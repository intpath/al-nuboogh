# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class noboogh(models.Model):
#     _name = 'noboogh.noboogh'
#     _description = 'noboogh.noboogh'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class Cus_nuboogh(models.Model):
    _inherit="account.move"
    warehouse_location_id = fields.Many2one('stock.picking',compute='calc_warehouse_location_id')

    @api.depends("partner_id")
    def calc_warehouse_location_id(self):
        transfers=self.env["stock.picking"].search([("origin","=",self.name)],limit=1)
        self.warehouse_location_id = transfers.id



class ProductType(models.Model):
    _inherit ='account.move'
    total_qty = fields.Float(compute="count_sold_item")  
    # country_of_origin = fields.Char(string="Manfacture Country")        
    # product_name_2 = fields.Char(string="Product Description")

    @api.depends("invoice_line_ids")
    def count_sold_item(self):
        total_qty = 0
        for line in self.invoice_line_ids:
            total_qty += line.quantity
        self.total_qty = total_qty     
    # product_type = fields.Selection([("consu","Consumer"),("service","Service"),("product","Product")],related="product_id.type",string="Product Type")


class ProductTemplateExt(models.Model):
    _inherit = 'product.template'
    product_type = fields.Char(string="نوع المنتج")    
    country_of_origin = fields.Char(string="بلد المنشأ")        
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج")


# class CustomerDueAmoutExt(models.Model):
#     _inherit = 'res.partner'
#     amount_due = fields.Float('res.partner',compute="compute_due")
#     price_subtotal = fields.Float('res.partner',compute="compute_due")

#     @api.depends()
#     def compute_due(self):
#         partner = self.env['res.partner'].search([("origin","=",self.name)], limit=1)
#         self.amount_due = partner.id
        
#         partner = self.env['res.partner'].search([("origin","=",self.name)], limit=1)
#         self.invoiced_due = partner.id

#         if amount_due:
#             total_due = price_subtotal-amount_due



class ResPartnerExt(models.Model):
    _inherit = "account.move"
    invoice_type = fields.Selection([('monetory', 'نقدي'), ('temem','ذمم')] , string="نوع الفاتورة" , default="temem")

