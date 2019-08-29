from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom

from odoo import tools
import base64
import datetime

# 何钰霖 计科162 161002219
class HRStore(http.Controller):
    @http.route('/supplier_addProduct', type='http', method='POST', website=True, auth="public")
    def addProduct(self, **post):
        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        return request.render('HRStore.supplier_addProduct', {
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_add', method="post")
    def supplier_addProduct(self, **post):
        name = post.get('pro_name')
        price = post.get('pro_price')
        detail = post.get('pro_detail')
        type = post.get('pro_type')
        state = '0'
        view = 0
        image_route = post.get('pro_image')
        if ':' in image_route:
            print(image_route)
        else:
            image_route = "D://picture//" + image_route
        print(image_route)
        pro_image = tools.image_resize_image_big(base64.b64encode(open(image_route, 'rb').read()))

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        request.env['hrstore.product'].sudo().create({'pro_name': name, 'pro_price': price, 'pro_detail': detail,
                                                      'pro_type': type, 'state': state, 'pro_view': view,
                                                      'user_id': userID,
                                                      'pro_image': pro_image})

        return request.render('HRStore.supplier_addProduct', {
            'message': "产品添加成功",
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_updateInfo', type='http', method='POST', website=True, auth="public")
    def updateProduct(self, **post):
        username = post.get('user_id')
        print(username)

        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        telephone = supplier.telephone
        print(telephone)

        return request.render('HRStore.supplier_updateInfo', {
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_updatepwd', type='http', method='POST', website=True, auth="public")
    def updatePWD(self, **post):
        old_pwd = post.get('old_pwd')
        new_pwd = post.get('new_pwd')
        ensure_pwd = post.get('ensure_pwd')

        username = post.get('user_id')
        user = request.env['hrstore.user'].search([('user_id', '=', username)])
        password = user.password

        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])


        if password != old_pwd:
            return request.render('HRStore.supplier_updateInfo', {
                'message': "原始密码输入错误",
                'supplier': supplier,
                'user_id': username
            })

        if new_pwd != ensure_pwd:
            return request.render('HRStore.supplier_updateInfo', {
                'message': "新密码与确认密码输入不符",
                'supplier': supplier,
                'user_id': username
            })

        info = {'password': new_pwd}
        user.write(info)
        return request.render('HRStore.supplier_updateInfo', {
            'message': "密码更新成功",
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_updateDetailed',type='http', method='POST', website=True, auth="public")
    def updateDetailed(self, **post):
        shopname = post.get('shopname')
        telephone = post.get('telephone')
        address = post.get('address')
        image_route = post.get('user_image')
        if ':' in image_route:
            print(image_route)
        else:
            image_route = "D://picture//" + image_route
        print(image_route)
        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        if image_route:
            user_image = tools.image_resize_image_big(base64.b64encode(open(image_route, 'rb').read()))
            info = {'shopname': shopname, 'telephone': telephone, 'address': address, 'user_image': user_image}
            supplier.write(info)
        else:
            info = {'shopname': shopname, 'telephone': telephone, 'address': address}
            supplier.write(info)

        request.session['telephone'] = supplier.telephone
        request.session['address'] = supplier.address
        request.session['user_image'] = supplier.user_image

        supplier_new = request.env['hrstore.shop'].search([('user_id', '=', username)])
        print(supplier_new.address)

        return request.render('HRStore.supplier_updateInfo', {
            'message': "个人信息修改成功",
            'supplier': supplier_new,
            'user_id': username
        })

    @http.route('/supplier_changeStatus', type='http', method='POST', website=True, auth="public")
    def changeStatus(self, **post):
        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '0')])
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        published_products = []
        for product in products:
            product_time = datetime.datetime.strptime(str(product.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            product_time = (product_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(product_time)
            temp.append(product)
            published_products.append(temp)
            print(product.pro_name)
            print(product.pro_image)

        return request.render('HRStore.supplier_changeStatus', {
            'products': published_products,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/deleteProduct',type='http', method='POST', website=True, auth="public")
    def deleteProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        request.env['hrstore.product'].search([('id', '=', pro_id)]).unlink()

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '0')])
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        published_products = []
        for product in products:
            product_time = datetime.datetime.strptime(str(product.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            product_time = (product_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(product_time)
            temp.append(product)
            published_products.append(temp)
            print(product.pro_name)
            print(product.pro_image)

        return request.render('HRStore.supplier_changeStatus', {
            'products': published_products,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_publishedProduct', type='http', method='POST', website=True, auth="public")
    def publisedProduct(self, **post):
        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        print(userID)

        published_products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])
        products = []
        for product in published_products:
            product_time = datetime.datetime.strptime(str(product.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
            product_time = (product_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = []
            temp.append(product_time)
            temp.append(product)
            products.append(temp)
            print(product.pro_name)
            print(product.pro_image)

        return request.render('HRStore.supplier_publishedProduct', {
            'published_products': products,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/deletePublishedProduct', type='http', method='POST', website=True, auth="public")
    def deletePublishedProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        request.env['hrstore.product'].search([('id', '=', int(pro_id))]).unlink()
        print(pro_id)

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        return request.render('HRStore.supplier_publishedProduct', {
            'published_products': products,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/updatePublishedProduct', type='http', method='POST', website=True, auth="public")
    def updatePublishedProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        print(product.pro_detail)

        return request.render('HRStore.supplier_updatePublishedProduct', {
            'product': product,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/updateProduct', type='http', method='POST', website=True, auth="public")
    def update(self, **post):
        pro_id = post.get('pro_id')
        print('xx')
        print(pro_id)

        name = post.get('pro_name')
        price = post.get('pro_price')
        detail = post.get('pro_detail')
        type = post.get('pro_type')
        image_route = post.get('pro_image')

        print(image_route)
        print(name)

        product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        if image_route:
            if ':' in image_route:
                print(image_route)
            else:
                image_route = "D://picture//" + image_route
            print(image_route)
            pro_image = tools.image_resize_image_big(base64.b64encode(open(image_route, 'rb').read()))
            info = {'pro_name': name, 'pro_price': price, 'pro_detail': detail, 'pro_type': type,
                    'pro_image': pro_image}

            product.write(info)
        else:
            info = {'pro_name': name, 'pro_price': price, 'pro_detail': detail, 'pro_type': type}
            product.write(info)

        new_product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        return request.render('HRStore.supplier_updatePublishedProduct', {
            'product': new_product,
            'message': '产品信息更新成功',
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/supplier_orderlist', type='http', method='POST', website=True, auth="public")
    def orderlist(self, **post):
        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        orderinfos = []
        for product in products:
            proID = product.id
            orders = request.env['hrstore.order'].search([('pro_id', '=', proID)])

            for order in orders:
                pro_ID = order.pro_id.id
                print(proID)
                product_search = request.env['hrstore.product'].search([('id', '=', pro_ID)])

                consumerID = request.env['hrstore.commonuser'].search([('id', '=', order.user_id.id)])

                orderinfo = []

                orderinfo.append(consumerID.username)
                orderinfo.append(product_search.pro_name)
                orderinfo.append(product_search.pro_price)
                orderinfo.append(product_search.pro_type)
                orderinfo.append(product_search.id)
                order_time = datetime.datetime.strptime(str(order.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                order_time = (order_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                orderinfo.append(order_time)
                orderinfo.append(order.state)
                orderinfo.append(order.id)
                orderinfo.append(order.order_price)

                orderinfos.append(orderinfo)

        return request.render('HRStore.supplier_orderlist', {
            'orders': orderinfos,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/ChangeOrder', type='http', method='POST', website=True, auth="public")
    def changeOrder(self, **post):
        print("进入修改状态页面")
        orderID = post.get('order_id')

        target = request.env['hrstore.order'].search([('id', '=', orderID)])
        info = {'state': '1'}
        target.write(info)

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        orderinfos = []
        for product in products:
            proID = product.id
            orders = request.env['hrstore.order'].search([('pro_id', '=', proID)])

            for order in orders:
                pro_ID = order.pro_id.id
                print(proID)
                product_search = request.env['hrstore.product'].search([('id', '=', pro_ID)])

                consumerID = request.env['hrstore.commonuser'].search([('id', '=', order.user_id.id)])

                orderinfo = []

                orderinfo.append(consumerID.username)
                orderinfo.append(product_search.pro_name)
                orderinfo.append(product_search.pro_price)
                orderinfo.append(product_search.pro_type)
                orderinfo.append(product_search.id)
                order_time = datetime.datetime.strptime(str(order.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                order_time = (order_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                orderinfo.append(order_time)
                orderinfo.append(order.state)
                orderinfo.append(order.id)
                orderinfo.append(order.order_price)

                orderinfos.append(orderinfo)

        return request.render('HRStore.supplier_orderlist', {
            'orders': orderinfos,
            'supplier': supplier,
            'user_id': username
        })

    @http.route('/ChangeOrderPrice', type='http', method='POST', website=True, auth="public")
    def deleteRoute(self, **post):
        print("进入修改价格页面")
        orderID = post.get('order_id')
        price = post.get('order_price')

        target = request.env['hrstore.order'].search([('id', '=', orderID)])
        info = {'order_price': price}
        target.write(info)

        username = post.get('user_id')
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        orderinfos = []
        for product in products:
            proID = product.id
            orders = request.env['hrstore.order'].search([('pro_id', '=', proID)])

            for order in orders:
                pro_ID = order.pro_id.id
                print(proID)
                product_search = request.env['hrstore.product'].search([('id', '=', pro_ID)])

                consumerID = request.env['hrstore.commonuser'].search([('id', '=', order.user_id.id)])

                orderinfo = []

                orderinfo.append(consumerID.username)
                orderinfo.append(product_search.pro_name)
                orderinfo.append(product_search.pro_price)
                orderinfo.append(product_search.pro_type)
                orderinfo.append(product_search.id)
                order_time = datetime.datetime.strptime(str(order.create_date)[0:19], '%Y-%m-%d %H:%M:%S')
                order_time = (order_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                orderinfo.append(order_time)
                orderinfo.append(order.state)
                orderinfo.append(order.id)
                orderinfo.append(order.order_price)

                orderinfos.append(orderinfo)

        return request.render('HRStore.supplier_orderlist', {
            'orders': orderinfos,
            'supplier': supplier,
            'user_id': username
        })
