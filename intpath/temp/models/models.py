# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"

    include_iqd_pricing_in_accounting = fields.Boolean("Include IQD Pricing in Account Moves", copy=False)