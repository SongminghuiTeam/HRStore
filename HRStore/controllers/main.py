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
        password_confirm = post.get('password_confirm')
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
            if password != password_confirm:
                return request.render('HRStore.sign_up', {
                    'message': "密码不匹配"
                })
            else:
                request.env['hrstore.user'].sudo().create(
                    {'user_id': user_id, 'password': password, 'user_type': user_type})
                if user_type == '1':
                    request.env['hrstore.commonuser'].sudo().create(
                        {'username': username, 'telephone': telephone, 'user_id': user_id})
                else:
                    request.env['hrstore.shop'].sudo().create(
                        {'shopname': username, 'telephone': telephone, 'user_id': user_id})
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
        request.session['product1_num'] = product1_num
        request.session['product2_num'] = product2_num
        request.session['product3_num'] = product3_num
        request.session['product4_num'] = product4_num

        return request.render('HRStore.products', {
            'products': all_products,
            'type': type,

        })

    # 进入我的
    @http.route('/user_profile', auth="public", type='http', website=True)
    def user_profile(self, **post):
        print("进入我的")
        username = post.get('user_id')
        print(username)
        userslist = request.env['hrstore.user'].search([('user_id', '=', username)])
        if len(userslist) != 0:
            user = userslist[0]
            if user.user_type == "1":
                # 改成转跳到普通用户的
                commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', username)])  # 用户详细信息
                cart_records = request.env['hrstore.cart'].sudo().search([('user_id', '=', username)])  # 购物车信息
                cart_products = []
                for cart_record in cart_records:
                    product_info = request.env['hrstore.product'].sudo().search([('state', '=', "1"), ('id', '=', cart_record.pro_id)])
                    shop_info = request.env['hrstore.shop'].sudo().search([('id', '=', product_info.user_id.id)]) 
                    cart_product = []
                    cart_product.append(product_info)
                    cart_product.append(cart_record.cart_num)
                    cart_product.append(shop_info.shopname)
                    cart_product.append(cart_record.id)
                    #print(cart_record.id)
                    cart_products.append(cart_product)
                return request.render('HRStore.customer_info', {
                    'user_info': user,
                    'commonuser_info': commonuser,
                    'cart_products': cart_products
                })
            elif user.user_type == '2':
                supplier = request.env['hrstore.shop'].search([('shopname', '=', username)])
                request.session['telephone'] = supplier.telephone
                return request.render('HRStore.supplier_addProduct')

        return request.render('HRStore.customer_service')

    # 首页查找
    @http.route('/search', type='http', method='POST', website=True, auth="public")
    def search(self, **post):
        pro_name = post.get('pro_name')
        all_products = request.env['hrstore.product'].search([('state', '=', "1"), ('pro_name', 'ilike', pro_name)])
        return request.render('HRStore.home', {
            'products': all_products
        })

    # 产品页查找
    @http.route('/search_product', type='http', method='POST', website=True, auth="public")
    def search_product(self, **post):
        pro_name = post.get('pro_name')
        type = post.get('type')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('pro_name', 'ilike', pro_name), ('pro_type', '=', type)])


        return request.render('HRStore.products', {

            'type': type,
            'products': all_products
        })

    # 显示产品的详细信息
    @http.route('/product_detail', type='http', method='POST', website=True, auth="public")
    def product_detail(self, **post):
        pro_id = post.get('product_id')
        # 获取产品的详细信息
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])

        # 获取产品的评论
        orders = request.env['hrstore.order'].search(
            [('pro_id', '=', pro_id)])
        all_comments = []
        for order in orders:
            comments = request.env['hrstore.comment'].search(
                [('order_id', '=', order.id)])
            for comment in comments:
                all_comments.append(comment)

        print(all_comments)
        for comment in all_comments:
            print(comment)
        if len(all_products) != 0:
            product = all_products[0]
            # 获取商家的信息
            user = request.env['hrstore.shop'].search(
                [('id', '=', product.user_id.id)])
            return request.render('HRStore.product_detail', {
                'product': product,
                'comments': all_comments,
                'shop_user': user
            })

    # 预购功能
    @http.route('/pre_order', type='http', method='POST', website=True, auth="public")
    def pre_order(self, **post):
        user_id = post.get('user_id')
        pro_id = post.get('product_id')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        if len(all_products) != 0:
            product = all_products[0]
        order_price = product.pro_price
        if user_id:
            user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
            user2 = request.env['hrstore.user'].search([('user_id', '=', user_id)])
            if user2.user_type=='2':
                message = "请使用普通用户账号登录"
            else:
                message = "预购成功,订单待处理......"
                request.env['hrstore.order'].sudo().create(
                    {'state': '0', 'order_price': order_price, 'user_id': user.id, 'pro_id': pro_id})
        else:
            message = "请先登录"

        return request.render('HRStore.product_detail', {
            'product': product,
            'message': message
        })

    # 加入购物车功能
    @http.route('/add_cart', type='http', method='POST', website=True, auth="public")
    def add_cart(self, **post):
        user_id = post.get('user_id')
        pro_id = post.get('product_id')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        if len(all_products) != 0:
            product = all_products[0]
        if user_id:
            user = request.env['hrstore.user'].search([('user_id', '=', user_id)])
            if user.user_type == '2':
                message = "请使用普通用户账号登录"
            else:
                message = "成功加入购物车"
                # 查找该用户的cart中是否已经存在该商品
                cart_records = request.env['hrstore.cart'].search([('user_id', '=', user_id),('pro_id', '=', pro_id)])
                if len(cart_records) != 0:
                    cart_record = cart_records[0]
                    num = cart_record.cart_num+1
                    info={'cart_num': num}
                    cart_record.write(info)
                else:
                    request.env['hrstore.cart'].sudo().create(
                        {'user_id': user_id, 'pro_id': pro_id})
        else:
            message = "请先登录"

        return request.render('HRStore.product_detail', {
            'product': product,
            'message': message
        })
