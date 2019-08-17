from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo import tools
import base64


class Customer(http.Controller):
    # 访问个人信息修改页面
    @http.route('/customer_modifyInfo', type='http', method='POST', website=True, auth="public")
    def customerInfo_modify(self, **post):
        user_id = request.session['user_id']
        userslist = request.env['hrstore.user'].sudo().search([('user_id', '=', user_id)])
        user = userslist[0]  # 用户信息
        commonuserlist = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])
        commonuser = commonuserlist[0]  # 用户详细信息

        return request.render('HRStore.customer_modifyInfo', {
            'user_info': user,
            'commonuser_info': commonuser
        })

    # 修改个人信息
    @http.route('/commonuser_modifyDetailed', type='http', method='POST', website=True, auth="public")
    def modifyDetailed(self, **post):
        user_image = post.get('user_image')
        image = request.registry['ir.attachment']
        name = post.get('user_image').filename
        username = post.get('username')
        telephone = post.get('telephone')
        address = post.get('address')
        user_id = request.session['user_id']
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])

        info = {'user_image': user_image, 'username': username, 'telephone': telephone, 'address': address}
        commonuser.write(info)

        commonuser_new = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])
        user = request.env['hrstore.user'].sudo().search([('user_id', '=', user_id)])

        return request.render('HRStore.customer_modifyInfo', {
                'message': "个人信息修改成功",
                'user_info': user,
                'commonuser_info': commonuser_new
            })

    # 修改密码
    @http.route('/costomer_modifypwd', type='http', method='POST', website=True, auth="public")
    def modifyPWD(self, **post):
        old_pwd = post.get('old_pwd')
        new_pwd = post.get('new_pwd')
        ensure_pwd = post.get('ensure_pwd')

        print(old_pwd)
        print(new_pwd)
        print(ensure_pwd)

        user_id = request.session['user_id']
        user = request.env['hrstore.user'].sudo().search([('user_id', '=', user_id)])
        password = user.password

        customer = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])
        user = request.env['hrstore.user'].sudo().search([('user_id', '=', user_id)])
        print(customer.user_image)
        print(customer.username)
        print(customer.address)
        print(customer.telephone)

        if password != old_pwd:
            return request.render('HRStore.customer_modifyInfo', {
                'message': "原始密码输入错误",
                'user_info': user,
                'commonuser_info': customer
            })

        if new_pwd != ensure_pwd:
            return request.render('HRStore.customer_modifyInfo', {
                'message': "新密码与确认密码输入不符",
                'user_info': user,
                'commonuser_info': customer
            })

        info = {'password': new_pwd}
        user.write(info)
        return request.render('HRStore.customer_modifyInfo', {
            'message': "密码更新成功",
            'user_info': user,
            'commonuser_info': customer
        })

    # 删除购物车
    @http.route('/cart_product_delete', type='http', method='POST', website=True, auth="public")
    def delete_cart_product(self, **post):
        print("删除购物车")
        cart_id = post.get('cart_id')
        print(cart_id)


        user_id = request.session['user_id']
        user = request.env['hrstore.user'].search([('user_id', '=', user_id)])    # 用户信息
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])  # 用户详细信息
        cart_records = request.env['hrstore.cart'].sudo().search([('user_id', '=', user_id)])  # 购物车信息
        cart_products = []
        request.env['hrstore.cart'].sudo().search([('id', '=', cart_id)]).unlink()      # 删除

        ###
        user_id = request.session['user_id']
        user = request.env['hrstore.user'].search([('user_id', '=', user_id)])    # 用户信息
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])  # 用户详细信息
        cart_records = request.env['hrstore.cart'].sudo().search([('user_id', '=', user_id)])  # 购物车信息
        cart_products = []

        for cart_record in cart_records:
            product_info = request.env['hrstore.product'].sudo().search(
                [('state', '=', "1"), ('id', '=', cart_record.pro_id)])
            shop_info = request.env['hrstore.shop'].sudo().search(
                [('id', '=', product_info.user_id.id)])
            cart_product = []
            cart_product.append(product_info)
            cart_product.append(cart_record.cart_num)
            cart_product.append(shop_info.shopname)
            cart_product.append(cart_record.id)
            cart_products.append(cart_product)

        return request.render('HRStore.customer_info', {
            'user_info': user,
            'commonuser_info': commonuser,
            'cart_products': cart_products
        })

    # 购买
    @http.route('/cart_product_purchase', type='http', method='POST', website=True, auth="public")
    def purchase_cart_product(self, **post):
        print("购买")
        user_id = post.get('user_id')
        pro_id = post.get('product_id')
        cart_id = post.get('cart_id')
        pro_num = post.get('pro_num')
        print(user_id)
        print(pro_id)
        print(cart_id)
        print(pro_num)

        all_products = request.env['hrstore.product'].search(
            [('state', '=', "1"), ('id', '=', pro_id)])
        if len(all_products) != 0:
            product = all_products[0]
        order_price = product.pro_price * int(pro_num)

        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
        request.env['hrstore.order'].sudo().create({'state': '0', 'order_price': order_price, 'user_id': user.id, 'pro_id': pro_id})
        request.env['hrstore.cart'].sudo().search([('id', '=', cart_id)]).unlink()

        message = "购买成功,订单待处理......"
        ###
        user = request.env['hrstore.user'].search([('user_id', '=', user_id)])    # 用户信息
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])  # 用户详细信息
        cart_records = request.env['hrstore.cart'].sudo().search([('user_id', '=', user_id)])  # 购物车信息
        cart_products = []

        for cart_record in cart_records:
            product_info = request.env['hrstore.product'].sudo().search(
                [('state', '=', "1"), ('id', '=', cart_record.pro_id)])
            shop_info = request.env['hrstore.shop'].sudo().search(
                [('id', '=', product_info.user_id.id)])
            cart_product = []
            cart_product.append(product_info)
            cart_product.append(cart_record.cart_num)
            cart_product.append(shop_info.shopname)
            cart_product.append(cart_record.id)
            cart_products.append(cart_product)

        return request.render('HRStore.customer_info', {
            'message': message,
            'user_info': user,
            'commonuser_info': commonuser,
            'cart_products': cart_products
        })

    # 进入购物车
    @http.route('/cart', type='http', method='POST', website=True, auth="public")
    def cart(self, **post):
        print("进入购物车")
        username = request.session['user_id']
        user = request.env['hrstore.user'].search([('user_id', '=', username)])     # 用户基本信息
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
            cart_products.append(cart_product)
        return request.render('HRStore.customer_info', {
            'user_info': user,
            'commonuser_info': commonuser,
            'cart_products': cart_products
        })


    # 进入订单
    @http.route('/order', type='http', method='POST', website=True, auth="public")
    def order(self, **post):
        print("进入订单")
        user_id = request.session['user_id']

        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])        # user基本信息
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])   # user详细信息

        order_records = request.env['hrstore.order'].sudo().search([('user_id', '=', user_id)])  # 订单信息
        all_orders = []
        for order_record in order_records:
            print(order_record.pro_id.id)
            product_info = request.env['hrstore.product'].sudo().search([('id', '=', order_record.pro_id.id)])
            shop_info = request.env['hrstore.shop'].sudo().search([('id', '=', product_info.user_id.id)])
            one_order = []
            one_order.append(product_info)
            one_order.append(shop_info)
            one_order.append(order_record)
            if order_record.state == "1":
                one_order.append("已完成")
            else:
                one_order.append("待处理")
            num = '×' + str(int(order_record.order_price / product_info.pro_price))
            one_order.append(num)
            all_orders.append(one_order)

        return request.render('HRStore.customer_order', {
            'user_info': user,
            'commonuser_info': commonuser,
            'all_orders': all_orders
        })

    # 进入评论
    @http.route('/comment', type='http', method='POST', website=True, auth="public")
    def comment(self, **post):
        print("进入评论")
        user_id = request.session['user_id']
        order_id = post.get('order_id')

        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])

        return request.render('HRStore.customer_comment', {
            'user_info': user,
            'order_id': order_id
        })

    # 添加评论
    @http.route('/add_comment', type='http', method='POST', website=True, auth="public")
    def add_comment(self, **post):
        print("添加评价")
        user_id = post.get('user_id')
        order_id = post.get('order_id')
        content = post.get('content')
        user = request.env['hrstore.commonuser'].search([('user_id', '=', user_id)])
        commonuser = request.env['hrstore.commonuser'].sudo().search([('user_id', '=', user_id)])  # 用户详细信息
        request.env['hrstore.comment'].sudo().create({'content': content, 'username': commonuser.username, 'user_id': user.id, 'order_id': order_id})
        message = '评论成功'
        print(message)

        return request.render('HRStore.customer_comment', {
            'user_info': user,
            'order_id': order_id,
            'message': message
        })

    # 退出
    @http.route('/logout', type='http', method='POST', website=True, auth="public")
    def logout(self, **post):
        print("退出")
        return request.render('HRStore.login')