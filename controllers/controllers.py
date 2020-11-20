# -*- coding: utf-8 -*-
# from odoo import http


# class Noboogh(http.Controller):
#     @http.route('/noboogh/noboogh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/noboogh/noboogh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('noboogh.listing', {
#             'root': '/noboogh/noboogh',
#             'objects': http.request.env['noboogh.noboogh'].search([]),
#         })

#     @http.route('/noboogh/noboogh/objects/<model("noboogh.noboogh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('noboogh.object', {
#             'object': obj
#         })
