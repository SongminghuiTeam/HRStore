from odoo import http
from odoo.local_addons.HRStore.models.HR_Database import HRProduct, HRUser, HROrder
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom

class HRStore(http.Controller):
    @http.route('/supplier_addProduct', auth="public")
    def addProduct(self, **post):
        return request.render('HRStore.supplier_addProduct')

    @http.route('/supplier_add', method="post")
    def supplier_addProduct(self, **post):
        name = post.get('pro_name')
        price = post.get('pro_price')
        detail = post.get('pro_detail')
        type = post.get('pro_type')
        state = '0'
        view = 0
        image_route = post.get('image_route')

        print(image_route)

        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id
        print('userID:')
        print(userID)

        request.env['hrstore.product'].sudo().create({'pro_name': name, 'pro_price': price, 'pro_detail': detail,
                                                      'pro_type': type, 'state': state, 'pro_view': view,
                                                      'user_id': userID,
                                                      'image_route': image_route})

        return request.render('HRStore.supplier_addProduct', {'message': "产品添加成功"})

    @http.route('/supplier_updateInfo', auth="public")
    def updateProduct(self):
        username = request.session['user_id']
        print(username)

        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        telephone = supplier.telephone
        print(telephone)

        return request.render('HRStore.supplier_updateInfo', {
            'supplier': supplier
        })

    @http.route('/supplier_updatepwd', auth="public")
    def updatePWD(self, **post):
        old_pwd = post.get('old_pwd')
        new_pwd = post.get('new_pwd')
        ensure_pwd = post.get('ensure_pwd')

        username = request.session['user_id']
        user = request.env['hrstore.user'].search([('user_id', '=', username)])
        password = user.password

        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        print(username)
        print(supplier.address)
        print(supplier.telephone)

        if password != old_pwd:
            return request.render('HRStore.supplier_updateInfo', {
                'message': "原始密码输入错误",
                'supplier': supplier
            })

        if new_pwd != ensure_pwd:
            return request.render('HRStore.supplier_updateInfo', {
                'message': "新密码与确认密码输入不符",
                'supplier': supplier
            })

        info = {'password': new_pwd}
        user.write(info)
        return request.render('HRStore.supplier_updateInfo', {
                'message': "密码更新成功",
                'supplier': supplier
            })

    @http.route('/supplier_updateDetailed', method="post")
    def updateDetailed(self, **post):
        shopname = post.get('shopname')
        telephone = post.get('telephone')
        address = post.get('address')

        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])

        info = {'shopname': shopname, 'telephone': telephone, 'address': address}
        supplier.write(info)

        supplier_new = request.env['hrstore.shop'].search([('user_id', '=', username)])
        print(supplier_new.address)

        return request.render('HRStore.supplier_updateInfo', {
                'message': "个人信息修改成功",
                'supplier': supplier_new
            })

    @http.route('/supplier_changeStatus', method="post")
    def changeStatus(self):
        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '0')])

        return request.render('HRStore.supplier_changeStatus', {
            'products': products
        })

    @http.route('/deleteProduct', method="post")
    def deleteProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        request.env['hrstore.product'].search([('id', '=', pro_id)]).unlink()

        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '0')])

        return request.render('HRStore.supplier_changeStatus', {
            'products': products
        })

    @http.route('/supplier_publishedProduct', method="post")
    def publisedProduct(self):
        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        print(userID)

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        return request.render('HRStore.supplier_publishedProduct', {
            'published_products': products
        })

    @http.route('/deletePublishedProduct', method="post")
    def deletePublishedProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        request.env['hrstore.product'].search([('id', '=', pro_id)]).unlink()

        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id

        products = request.env['hrstore.product'].search([('user_id', '=', userID), ('state', '=', '1')])

        return request.render('HRStore.supplier_publishedProduct', {
            'published_products': products
        })

    @http.route('/updatePublishedProduct', method="post")
    def updatePublishedProduct(self, **post):
        pro_id = post.get('pro_id')
        print(pro_id)

        product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        print(product.pro_detail)

        return request.render('HRStore.supplier_updatePublishedProduct',{
            'product': product
        })

    @http.route('/updateProduct', method="post")
    def update(self, **post):
        pro_id = post.get('pro_id')
        print('xx')
        print(pro_id)

        name = post.get('pro_name')
        price = post.get('pro_price')
        detail = post.get('pro_detail')
        type = post.get('pro_type')



        product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        info = {'pro_name': name, 'pro_price': price, 'pro_detail': detail, 'pro_type': type}
        product.write(info)

        new_product = request.env['hrstore.product'].search([('id', '=', pro_id)])

        return request.render('HRStore.supplier_updatePublishedProduct', {
            'product': new_product,
            'message': '产品信息更新成功'
        })

    @http.route('/supplier_orderlist', method="post")
    def orderlist(self):
        username = request.session['user_id']
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
                orderinfo.append(order.create_date)
                orderinfo.append(order.state)
                orderinfo.append(order.id)

                orderinfos.append(orderinfo)

        return request.render('HRStore.supplier_orderlist', {
            'orders': orderinfos
        })

    @http.route('/ChangeOrder', method="post")
    def deleteRoute(self, **post):
        orderID = post.get('order_id')

        target = request.env['hrstore.order'].search([('id', '=', orderID)])
        info = {'state': '1'}
        target.write(info)

        username = request.session['user_id']
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
                orderinfo.append(order.create_date)
                orderinfo.append(order.state)
                orderinfo.append(order.id)

                orderinfos.append(orderinfo)

        return request.render('HRStore.supplier_orderlist', {
            'orders': orderinfos
        })