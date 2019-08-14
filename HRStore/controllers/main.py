# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom


class Hello(http.Controller):
    # 注册页面
    @http.route('/register', type='http', method='POST', website=True, auth="public")
    def register(self, **post):
        user_id = post.get('user_id')
        password = post.get('password')
        user_type = post.get('user_type')
        username = post.get('username')
        telephone = post.get('telephone')

        # 判断数据库中是否已经存在该账号
        users = request.env['hrstore.user'].search([('user_id', '=', user_id)])
        if len(users) != 0:
            return request.render('HRStore.sign_up', {
                'message': "该账号已存在"
            })
        else:
            request.env['hrstore.user'].sudo().create(
                {'user_id': user_id, 'password': password, 'user_type': user_type})
            if user_type == '1':
                request.env['hrstore.commonuser'].sudo().create(
                    {'username': username, 'telephone': telephone, 'user_id': user_id})
            else:
                request.env['hrstore.shop'].sudo().create(
                    {'username': username, 'telephone': telephone, 'user_id': user_id})
            return request.render('HRStore.login')

    # 访问登录页面
    @http.route('/login', auth="public")
    def login(self):
        return request.render('HRStore.login')

    # 访问注册页面
    @http.route('/sign_up', auth="public")
    def sign_up(self):
        return request.render('HRStore.sign_up')

    # 访问客服页面
    @http.route('/customer_service', auth="public")
    def customer_service(self):
        return request.render('HRStore.customer_service')

    # 通过链接直接访问首页
    @http.route('/home', type='http', method='POST', website=True, auth="public")
    def home(self, **post):
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])
        print("home")
        return request.render('HRStore.home', {
            'products': all_products
        })

    # 通过登录页面的登录按钮访问
    @http.route('/login_home', type='http', method='POST', website=True, auth="public")
    def login_home(self, **post):
        username = post.get('username')
        password = post.get('password')
        userslist = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)])
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])

        if len(userslist) != 0:
            request.session['user_id'] = username
            return request.render(
                'HRStore.home',
                {
                    'products': all_products
                }
            )
        return request.render('HRStore.login', {

            'message': "用户名或密码错误！"
        })

    @http.route('/products', auth="public", type='http', website=True)
    def get_products(self, **post):

        type = post.get('type')
        all_products = request.env['hrstore.product'].search([('pro_type', '=', type), ('state', '=', "1")])
        product1_num = request.env['hrstore.product'].search_count([('pro_type', '=', "1"), ('state', '=', "1")])
        product2_num = request.env['hrstore.product'].search_count([('pro_type', '=', "2"), ('state', '=', "1")])
        product3_num = request.env['hrstore.product'].search_count([('pro_type', '=', "3"), ('state', '=', "1")])
        product4_num = request.env['hrstore.product'].search_count([('pro_type', '=', "4"), ('state', '=', "1")])
        return request.render('HRStore.products', {
            'products': all_products,
            'product1_num': product1_num,
            'product2_num': product2_num,
            'product3_num': product3_num,
            'product4_num': product4_num,
            'type': type,

        })

    # 进入我的
    @http.route('/user_profile', auth="public", type='http', website=True)
    def user_profile(self, **post):
        username = post.get('user_id')
        print(username)
        userslist = request.env['hrstore.user'].search([('user_id', '=', username)])
        if len(userslist) != 0:
            user = userslist[0]
            if user.user_type == 1:
                # 改成转跳到普通用户的
                return request.render('HRStore.customer_service')
            elif user.user_type == 2:
                # 改成转跳到供应商的
                return request.render('HRStore.customer_service')

        return request.render('HRStore.customer_service')

    # 首页查找
    @http.route('/search', type='http', method='POST', website=True, auth="public")
    def search(self, **post):
        pro_name = post.get('pro_name')
        all_products = request.env['hrstore.product'].search([('state', '=', "1"), ('pro_name', '=', pro_name)])
        return request.render('HRStore.home', {
            'products': all_products
        })

    # 产品页查找
    @http.route('/search_product', type='http', method='POST', website=True, auth="public")
    def search_product(self, **post):
        pro_name = post.get('pro_name')
        type = post.get('type')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('pro_name', '=', pro_name), ('pro_type', '=', type)])
        return request.render('HRStore.home', {
            'products': all_products
        })

    # 显示产品的详细信息
    @http.route('/product_detail', type='http', method='POST', website=True, auth="public")
    def product_detail(self, **post):
        pro_id = post.get('product_id')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        if len(all_products) != 0:
            product = all_products[0]
            return request.render('HRStore.product_detail', {
                'product': product
            })
