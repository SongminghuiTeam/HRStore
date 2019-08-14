# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom


class Hello(http.Controller):
    @http.route('/login', auth="public")
    def login(self, **post):
        user = post.get('user')
        return request.render('HRStore.login', {
            'user': user, })

    @http.route('/sign_up', auth="public")
    def sign_up(self, **post):
        user = post.get('user')
        return request.render('HRStore.sign_up', {
            'user': user, })

    @http.route('/customer_service', auth="public")
    def sign_up(self, **post):
        user = post.get('user')
        return request.render('HRStore.customer_service', {
            'user': user, })

    # 访问首页，由链接直接转跳
    @http.route('/home', type='http', method='POST', website=True, auth="public")
    def home(self, **post):
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])
        user = post.get('user')
        print("home")
        print(user)
        return request.render('HRStore.home', {
            'user': user,
            'products': all_products
        })

    # 访问首页，由登录页面跳转
    @http.route('/login_home', type='http', method='POST', website=True, auth="public")
    def login_home(self, **post):
        username = post.get('username')
        password = post.get('password')
        # request.env['hrstore.user'].sudo().create({'user_id': username, 'password': password})
        # user = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)]),
        userslist = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)])
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])

        user = post.get('user')
        print("login_home")
        print(user)
        print("###############")
        print(userslist)
        if len(userslist) != 0:
            user = userslist[0]
            return request.render(
                'HRStore.home',
                {'user': username,
                 'products': all_products
                 }
            )
        return request.render('HRStore.login', {
            'no_user': True,
            'user': user
        })

    # 访问特定类型产品的页面
    @http.route('/products', auth="public", type='http', website=True)
    def get_products(self, **post):
        type = post.get('type')
        user = post.get('user')
        if user.isspace():
            user=None
        user = post.get('user')
        print("product")
        print(user)
        all_products = request.env['hrstore.product'].search([('pro_type', '=', type), ('state', '=', "1")])
        products1 = request.env['hrstore.product'].search([('pro_type', '=', "1"), ('state', '=', "1")])
        products2 = request.env['hrstore.product'].search([('pro_type', '=', "2"), ('state', '=', "1")])
        products3 = request.env['hrstore.product'].search([('pro_type', '=', "3"), ('state', '=', "1")])
        products4 = request.env['hrstore.product'].search([('pro_type', '=', "4"), ('state', '=', "1")])
        return request.render('HRStore.products', {
            'products': all_products,
            'products1_num': len(products1),
            'products2_num': len(products2),
            'products3_num': len(products3),
            'products4_num': len(products4),
            'type': type,
            'user': user
        })
