# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    warehouse_location_id = fields.Many2one(
        'stock.picking', compute='calc_warehouse_location_id')
    total_qty = fields.Integer(compute="count_sold_item")
    invoice_type = fields.Selection(
        [('monetory', 'نقدي'), ('temem', 'ذمم')], string="نوع الفاتورة", default="temem")
    
    iqd_currency_id = fields.Many2one("res.currency", "IQD Currency", compute="get_iqd_currency")
    
    partner_due = fields.Monetary(
        string="Partner due", compute="_compute_partner_due", currency_field="company_currency_id")
    partner_due_iqd = fields.Monetary(
        string="Partner due (IQD)", compute="_compute_partner_due", currency_field="iqd_currency_id")

    previous_customer_debit = fields.Monetary(string="Previous Customer Debit", compute="_get_prev_debit", currency_field="company_currency_id")
    iqd_previous_customer_debit = fields.Monetary(string="Previous Customer Debit (IQD)", compute="_get_prev_debit", currency_field="iqd_currency_id")

    # current_customer_debit = fields.Monetary(string="Current Customer Debit", compute="_get_curr_debit", currency_field="company_currency_id")
    # iqd_current_customer_debit = fields.Monetary(string="Current Customer Debit (IQD)", compute="_get_curr_debit", currency_field="iqd_currency_id")



    def get_iqd_currency(self):
        for move_id in self:
            move_id.iqd_currency_id = self.env.ref("base.IQD").id

    @api.depends('partner_id')
    def _compute_partner_due(self):
        account_partner_ledger = self.env['account.partner.ledger'].with_context(
            {'default_partner_id': self.partner_id.id})
        options = account_partner_ledger._get_options()
        options['partner_ids'] = [self.partner_id.id]
        lines = account_partner_ledger._get_partner_ledger_lines(options)
        total_balance = float(lines[-1]['columns'][-1]['name'].split()[-1].replace(',', ''))
        iqd_total_balance = self.company_currency_id._convert(
            total_balance,
            self.iqd_currency_id,
            self.company_id,
            self.date)
        self.partner_due = total_balance
        self.partner_due_iqd = iqd_total_balance

    @api.depends("partner_id")
    def _get_prev_debit(self):
        for account_move in self:
            if account_move.partner_id:
                if account_move.currency_id == account_move.iqd_currency_id:
                    account_move.previous_customer_debit = account_move.partner_due - account_move.currency_id._convert(
                        account_move.amount_total,
                        account_move.company_currency_id,
                        account_move.company_id,
                        account_move.date
                    )
                    account_move.iqd_previous_customer_debit = account_move.partner_due_iqd - account_move.amount_total
                else:
                    account_move.previous_customer_debit = account_move.partner_due - account_move.amount_total
                    account_move.iqd_previous_customer_debit = account_move.partner_due_iqd - account_move.currency_id._convert(
                        account_move.amount_total,
                        account_move.iqd_currency_id,
                        account_move.company_id,
                        account_move.date
                    )
            else:
                account_move.previous_customer_debit = False
                account_move.iqd_previous_customer_debit = False

    # @api.depends("partner_id")
    # def _get_curr_debit(self):
    #     for account_move in self:
    #         if account_move.partner_id:
    #             if account_move.currency_id == account_move.iqd_currency_id:
    #                 usd_amount_total = account_move.currency_id._convert(
    #                     account_move.amount_total,
    #                     account_move.company_currency_id,
    #                     account_move.company_id,
    #                     account_move.date
    #                 )
    #                 account_move.current_customer_debit = account_move.previous_customer_debit + usd_amount_total
    #                 account_move.iqd_current_customer_debit = account_move.iqd_previous_customer_debit + account_move.amount_total
    #             else:
    #                 account_move.current_customer_debit = account_move.previous_customer_debit + account_move.amount_total
    #                 account_move.iqd_current_customer_debit = account_move.iqd_previous_customer_debit + account_move.currency_id._convert(
    #                     account_move.amount_total,
    #                     account_move.iqd_currency_id,
    #                     account_move.company_id,
    #                     account_move.date
    #                 )
    #         else:
    #             account_move.current_customer_debit = False
    #             account_move.iqd_current_customer_debit = False



    @api.depends("partner_id")
    def calc_warehouse_location_id(self):
        if self.invoice_origin:
            transfers = self.env["stock.picking"].search(
                [("origin", "=", self.invoice_origin)], order="id desc", limit=1)
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

    partner_due = fields.Monetary(
        string="مستحق الزبون/المجهز", compute="_compute_partner_due", currency_field="company_currency_id")
    iqd_currency_id = fields.Many2one("res.currency", "IQD Currency", compute="get_iqd_currency")
    partner_due_iqd = fields.Monetary(
        string="Partner due in IQD currency", compute="_compute_partner_due", currency_field="iqd_currency_id")
    partner_id = fields.Many2one(
        domain="[('company_id', 'in', [main_company_id, False])]")
    company_currency_id = fields.Many2one(
        related="main_company_id.currency_id")
    main_company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, readonly=True)

    def get_iqd_currency(self):
        for move_id in self:
            move_id.iqd_currency_id = self.env.ref("base.IQD").id

    @api.onchange('partner_id')
    def _compute_partner_due(self):
        account_partner_ledger = self.env['account.partner.ledger'].with_context(
            {'default_partner_id': self.partner_id.id})
        options = account_partner_ledger._get_options()
        options['partner_ids'] = [self.partner_id.id]
        lines = account_partner_ledger._get_partner_ledger_lines(options)
        total_balance = float(lines[-1]['columns'][-1]['name'].split()[-1].replace(',', ''))
        iqd_total_balance = self.company_currency_id._convert(
            total_balance,
            self.iqd_currency_id,
            self.company_id,
            self.date)
        self.partner_due = total_balance
        self.partner_due_iqd = iqd_total_balance


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type = fields.Char(string="الموديل")
    product_type_en = fields.Char(string="الموديل بالإنكليزي")
    country_of_origin = fields.Char(string="بلد المنشأ")
    country_of_origin_en = fields.Char(string="بلد المنشأ بالإنكليزي")
    product_name_2 = fields.Char(string="الاسم الثاني للمنتج")
    name_en = fields.Char(string=" اسم المادة بالانكليزي")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    product_model_type = fields.Char(
        string="الموديل", related="product_id.product_type")
    product_country_of_origin = fields.Char(
        string="بلد المنشأ", related="product_id.country_of_origin")
    product_name_2 = fields.Char(
        string="الاسم الثاني للمنتج", related="product_id.product_name_2")


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_type_en = fields.Char(
        string="الموديل بالإنكليزي", related="product_id.product_type_en")
    product_country_of_origin_en = fields.Char(
        string="بلد المنشأ بالإنكليزي", related="product_id.country_of_origin_en")
    product_name_en = fields.Char(
        string=" اسم المادة بالانكليزي", related="product_id.name_en")


class ProductProduct(models.Model):
    _inherit = "product.product"

    display_name = fields.Char(compute="_compute_full_names")

    def _compute_full_names(self):
        for item in self:
            if item.product_name_2:
                item.display_name = item.name + " - " + item.product_name_2
            else:
                item.display_name = item.name

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.display_name))
        return result

class ResCompany(models.Model):
    _inherit = "res.company"

    include_iqd_pricing_in_accounting = fields.Boolean("Include IQD Pricing in Account Moves", copy=False)
