# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
import datetime


# 梁晓珂 计科162  161002221 和 宋明惠 计科162  161002226
class Hello(http.Controller):
    # 注册页面
    # 梁晓珂 计科162  161002221
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
    # 宋明惠
    @http.route('/login', auth="public")
    def login(self):
        return request.render('HRStore.login')

    # 访问注册页面
    # 宋明惠
    @http.route('/sign_up', auth="public")
    def sign_up(self):
        return request.render('HRStore.sign_up')

    # 访问客服页面
    # 宋明惠
    @http.route('/customer_service', auth="public")
    def customer_service(self, **post):
        user_id = post.get('user_id')
        print(user_id)
        return request.render('HRStore.customer_service',
                              {'user_id': user_id})

        # 通过链接直接访问首页
        # 宋明惠

    @http.route('/index', type='http', method='POST', website=True, auth="public")
    def index(self, **post):
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])
        print("home")
        return request.render('HRStore.home', {
            'products': all_products
        })

    # 访问首页
    # 宋明惠
    @http.route('/home', type='http', method='POST', website=True, auth="public")
    def home(self, **post):
        user_id = post.get('user_id')
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])
        print("home")
        return request.render('HRStore.home', {
            'products': all_products,
            'user_id': user_id
        })

    # 通过登录页面的登录按钮访问
    # 宋明惠
    @http.route('/login_home', type='http', method='POST', website=True, auth="public")
    def login_home(self, **post):
        username = post.get('username')
        password = post.get('password')
        userslist = request.env['hrstore.user'].search([('user_id', '=', username), ('password', '=', password)])
        all_products = request.env['hrstore.product'].search([('state', '=', "1")])

        if len(userslist) != 0:
            # request.session['user_id'] = username
            return request.render(
                'HRStore.home',
                {
                    'user_id': username,
                    'products': all_products
                }
            )
        return request.render('HRStore.login', {
            'user_id': username,
            'message': "用户名或密码错误！"
        })

    # 宋明惠
    @http.route('/products', auth="public", type='http', website=True)
    def get_products(self, **post):
        user_id = post.get('user_id')
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
            'user_id': user_id
        })

    # 进入我的
    # 宋明惠
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
                    product_info = request.env['hrstore.product'].sudo().search(
                        [('state', '=', "1"), ('id', '=', cart_record.pro_id)])
                    shop_info = request.env['hrstore.shop'].sudo().search([('id', '=', product_info.user_id.id)])
                    cart_product = []
                    cart_product.append(product_info)
                    cart_product.append(cart_record.cart_num)
                    cart_product.append(shop_info.shopname)
                    cart_product.append(cart_record.id)
                    # print(cart_record.id)
                    cart_products.append(cart_product)
                return request.render('HRStore.customer_info', {
                    'user_info': user,
                    'commonuser_info': commonuser,
                    'cart_products': cart_products,
                    'user_id': username
                })
            elif user.user_type == '2':
                supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
                print(supplier)
                return request.render('HRStore.supplier_addProduct', {
                    'supplier': supplier,
                    'user_id': username
                })

        return request.render('HRStore.login')

    # 首页查找
    # 梁晓珂
    @http.route('/search', type='http', method='POST', website=True, auth="public")
    def search(self, **post):
        user_id = post.get("user_id")
        pro_name = post.get('pro_name')
        all_products = request.env['hrstore.product'].search([('state', '=', "1"), ('pro_name', 'ilike', pro_name)])
        return request.render('HRStore.home', {
            'products': all_products,
            'user_id': user_id
        })

    # 产品页查找
    # 梁晓珂
    @http.route('/search_product', type='http', method='POST', website=True, auth="public")
    def search_product(self, **post):
        user_id = post.get("user_id")
        pro_name = post.get('pro_name')
        type = post.get('type')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('pro_name', 'ilike', pro_name), ('pro_type', '=', type)])

        return request.render('HRStore.products', {
            'user_id': user_id,
            'type': type,
            'products': all_products
        })

    # 显示产品的详细信息
    # 宋明惠
    @http.route('/product_detail', type='http', method='POST', website=True, auth="public")
    def product_detail(self, **post):
        user_id = post.get("user_id")
        pro_id = post.get('product_id')
        # 获取产品的详细信息
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        info = {'pro_view': all_products.pro_view + 1}
        all_products.write(info)

        # 获取产品的评论
        orders = request.env['hrstore.order'].search(
            [('pro_id', '=', int(pro_id))])
        print("################")
        print(pro_id)
        print(user_id)

        print(orders)
        all_comments = []
        for order in orders:
            print(order.id)
            comments = request.env['hrstore.comment'].search(
                [('order_id', '=', order.id)])
            for comment in comments:
                time = datetime.datetime.strptime(str(comment.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                print(time)
                temp = []
                temp.append(time)
                temp.append(comment)
                all_comments.append(temp)

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
                'shop_user': user,
                'user_id': user_id
            })

    # 预购功能
    # 梁晓珂
    @http.route('/pre_order', type='http', method='POST', website=True, auth="public")
    def pre_order(self, **post):
        user_id = post.get('user_id')
        pro_id = post.get('product_id')
        pro_type = post.get('pro_type')
        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        if len(all_products) != 0:
            product = all_products[0]
        order_price = product.pro_price
        if user_id:
            user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
            user2 = request.env['hrstore.user'].search([('user_id', '=', user_id)])
            if user2.user_type == '2':
                message = "请使用普通用户账号登录"
            else:
                if pro_type == '3':  # 如果是精美商品，可直接购买，跳到付款页面
                    addresses = request.env['hrstore.address'].search([('user_id', '=', user.id)])
                    return request.render('HRStore.confirm_order', {
                        'product': product,
                        'addresses': addresses,
                        'order_price': order_price,
                        'user_id': user_id,
                        'flag': '0'
                    })
                else:  # 其他产品，需要经过供应商确认订单，然后在“我的订单”中，进行购买
                    message = "预购成功,订单待处理......"
                    request.env['hrstore.order'].sudo().create(
                        {'state': '0', 'user_id': user.id, 'pro_id': pro_id})
        else:
            message = "请先登录"

        user = request.env['hrstore.shop'].search(
            [('id', '=', product.user_id.id)])

        # 获取产品的评论
        orders = request.env['hrstore.order'].search(
            [('pro_id', '=', pro_id)])
        all_comments = []
        for order in orders:
            comments = request.env['hrstore.comment'].search(
                [('order_id', '=', order.id)])
            for comment in comments:
                time = datetime.datetime.strptime(str(comment.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                print(time)
                temp = []
                temp.append(time)
                temp.append(comment)
                all_comments.append(temp)

        return request.render('HRStore.product_detail', {
            'product': product,
            'comments': all_comments,
            'shop_user': user,
            'user_id': user_id,
            'message': message
        })

    # 加入购物车功能
    # 梁晓珂
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
                cart_records = request.env['hrstore.cart'].search([('user_id', '=', user_id), ('pro_id', '=', pro_id)])
                if len(cart_records) != 0:
                    cart_record = cart_records[0]
                    num = cart_record.cart_num + 1
                    info = {'cart_num': num}
                    cart_record.write(info)
                else:
                    request.env['hrstore.cart'].sudo().create(
                        {'user_id': user_id, 'pro_id': pro_id})
        else:
            message = "请先登录"

        user = request.env['hrstore.shop'].search(
            [('id', '=', product.user_id.id)])

        # 获取产品的评论
        orders = request.env['hrstore.order'].search(
            [('pro_id', '=', pro_id)])
        all_comments = []
        for order in orders:
            comments = request.env['hrstore.comment'].search(
                [('order_id', '=', order.id)])
            for comment in comments:
                time = datetime.datetime.strptime(str(comment.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                print(time)
                temp = []
                temp.append(time)
                temp.append(comment)
                all_comments.append(temp)

        return request.render('HRStore.product_detail', {
            'product': product,
            'comments': all_comments,
            'shop_user': user,
            'user_id': user_id,
            'message': message
        })


    # 转到添加收货地址页面
    # 梁晓珂
    @http.route('/to_add_address', type='http', method='POST', website=True, auth="public")
    def to_add_address(self, **post):
        user_id = post.get("user_id")
        product_id = post.get("product_id")
        return request.render('HRStore.add_address', {
            'user_id': user_id,
            'product_id': product_id
        })

    # 添加收货地址
    # 梁晓珂
    @http.route('/add_address', type='http', method='POST', website=True, auth="public")
    def add_address(self, **post):
        user_id = post.get("user_id")
        product_id = post.get("product_id")
        province = post.get("province")
        city = post.get("city")
        block = post.get("block")
        street = post.get("street")
        details = post.get("details")
        receiver_name = post.get("receiver_name")
        receiver_tel = post.get("receiver_tel")

        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
        request.env['hrstore.address'].sudo().create(
            {'province': province, 'city': city, 'block': block,
             'street': street, 'details': details, 'receiver_name': receiver_name, 'receiver_tel': receiver_tel,
             'user_id': user.id})

        product = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', product_id)])

        addresses = request.env['hrstore.address'].search([('user_id', '=', user.id)])

        return request.render('HRStore.confirm_order', {
            'product': product,
            'addresses': addresses,
            'order_price': product.pro_price,
            'user_id': user_id
        })

    # 提交订单--添加一条订单记录变成待付款状态1
    # 梁晓珂
    @http.route('/submit_order', type='http', method='POST', website=True, auth="public")
    def submit_order(self, **post):
        user_id = post.get("user_id")
        product_id = post.get("product_id")
        address_id = post.get("address_id")
        order_price = post.get('order_price')

        print(product_id)
        print(address_id)

        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])

        order = request.env['hrstore.order'].sudo().create(
            {'state': '1', 'user_id': user.id, 'pro_id': product_id, 'address_id': address_id, 'order_price': order_price})

        return request.render('HRStore.pay_order', {
            'user_id': user_id,
            'order_id': order.id
        })

        # 进入论坛
        # 宋明惠

    @http.route('/forum', type='http', method='POST', website=True, auth="public")
    def forum(self, **post):
        user_id = post.get('user_id')
        print(user_id)
        forum_list = request.env['hrstore.forum'].search([])

        forums = []
        for forum in forum_list:
            time = datetime.datetime.strptime(str(forum.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(time)
            temp.append(forum)
            forums.append(temp)

        ad_list = request.env['hrstore.ad'].search([])
        return request.render('HRStore.forum', {
            'user_id': user_id, 'forum_list': forums, 'ad_list': ad_list})

    # 添加论坛
    # 宋明惠
    @http.route('/add_forum', type='http', method='POST', website=True, auth="public")
    def add_forum(self, **post):
        user_id = post.get('user_id')
        title = post.get('title')
        content = post.get('content')
        label = post.get('label')
        print("user_id" + user_id)
        user = request.env['hrstore.user'].search([('user_id', '=', user_id)])
        print(user.id)
        print(user.user_type)
        if user.user_type == '1':
            username = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
            name = username.username
            request.env['hrstore.forum'].sudo().create(
                {'user_id': user.id, 'title': title, 'content': content, 'label': label, 'username': name})
        elif user.user_type == '2':
            username = request.env['hrstore.shop'].search([('user_id', '=', user_id)])
            name = username.shopname
            request.env['hrstore.forum'].sudo().create(
                {'user_id': user.id, 'title': title, 'content': content, 'label': label, 'username': name})
        forum_list = request.env['hrstore.forum'].search([])
        forums = []
        for forum in forum_list:
            time = datetime.datetime.strptime(str(forum.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(time)
            temp.append(forum)
            forums.append(temp)
        ad_list = request.env['hrstore.ad'].search([])
        return request.render('HRStore.forum', {
            'user_id': user_id, 'forum_list': forums, 'ad_list': ad_list})

    # 进入论坛特定标签的论坛
    # 宋明惠
    @http.route('/get_forum', type='http', method='POST', website=True, auth="public")
    def get_forum(self, **post):
        user_id = post.get('user_id')
        label = post.get('label')
        print("user_id" + user_id)
        forum_list = request.env['hrstore.forum'].search([('label', '=', label)])
        forums = []
        for forum in forum_list:
            time = datetime.datetime.strptime(str(forum.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            time = (time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(time)
            temp.append(forum)
            forums.append(temp)
        ad_list = request.env['hrstore.ad'].search([])
        return request.render('HRStore.forum', {
            'user_id': user_id, 'forum_list': forums, 'ad_list': ad_list})


    @http.route('/pay')
    def pay(self, **post):
        user_id = post.get('user_id')
        order_id = post.get('order_id')

        order = request.env['hrstore.order'].search([('id', '=', order_id)])
        info = {'state': '2'}
        order.write(info)

        return request.render('HRStore.pay_order', {
            'message': '付款成功',
            'user_id': user_id
        })