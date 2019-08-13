# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons_test.HRStore.models.HR_Database import HRUser
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom


class Hello(http.Controller):
    @http.route('/login', auth="public")
    def login(self):
        return request.render('HRStore.login')

    @http.route('/sign_up', auth="public")
    def sign_up(self):
        return request.render('HRStore.sign_up')

    @http.route('/home', type='http', method='POST', website=True, auth="public")
    def home(self, **post):
        username = post.get('username')
        password = post.get('password')
        # request.env['hrstore.user'].sudo().create({'user_id': username, 'password': password})
        # user = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)]),
        userslist = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)])
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])

        print("###############")
        print(userslist)
        if len(userslist) != 0:
            users = userslist[0]
            return request.render(
                    'HRStore.home',
                    {'user': users,
                     'no_user': False,
                     'products': all_products
                     }
                )
        return request.render('HRStore.home', {
            'no_user': True,
            'products': all_products
        })

    @http.route('/products', auth="public", type='http', website=True)
    def get_products(self, **post):
        type = post.get('type')
        all_products = request.env['hrstore.product'].search([('pro_type', '=', type), ('state', '=', "1")])

        return request.render('HRStore.products', {
            'products': all_products,
            'type':type
        })
