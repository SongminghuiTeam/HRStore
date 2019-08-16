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
        state = 0
        view = 0
        image = post.get('pro_image')

        username = request.session['user_id']
        supplier = request.env['hrstore.shop'].search([('user_id', '=', username)])
        userID = supplier.id
        print(userID)

        request.env['hrstore.product'].sudo().create({'pro_name': name, 'pro_price': price, 'pro_detail': detail,
                                                      'pro_type': type, 'state': state, 'pro_view': view,
                                                      'user_id': userID,
                                                      'pro_image': image})

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

