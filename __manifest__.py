# -*- coding: utf-8 -*-
{
    'name': "Al-Nuboogh",

    'summary': """
        Customizations for Al-Nuboogh""",

    'author': "INTEGRATED PATH",
    'website': "https://www.int-path.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'account', 'product', 'purchase', 'account_reports'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/account_move_view.xml',
        'views/product_product.xml',
        'views/account_payment_view.xml',
        'views/sale_purchase_view.xml',
        'views/res_company_views.xml',
        'reports/invoice_report.xml',
        'reports/custome_layout.xml',
        'reports/account_payment.xml',
        'reports/sale_order_report.xml',
        'reports/purchase_order_report.xml',
        'reports/stock_picking_report.xml',
        'reports/delivery_slip_report.xml',
    ],
}
