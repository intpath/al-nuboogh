# -*- coding: utf-8 -*-
{
    'name': "noboogh",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'stock', 'account', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_view.xml',
        'views/product_product.xml',
        'views/sale_purchase_view.xml',
        'reports/invoice_report.xml',
        'reports/custome_layout.xml',
        'reports/account_payment.xml',
        'reports/sale_order_report.xml',
        'reports/purchase_order_report.xml',
        'reports/stock_picking_report.xml',
    ],
}
