from odoo import http
from odoo.local_addons.HRStore.models.HR_Database import HRProduct
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom

class HRStore(http.Controller):
    @http.route('/supplier_addProduct', auth="public")
    def addProduct(self, **post):
        name = post.get('pro_name')
        price = post.get('pro_price')
        detail = post.get('pro_detail')
        type = post.get('pro_type')
        state = 0
        view = 0
        image = post.get('pro_image')
        username = post.get('userID')
        user = request.env['hrstore.user'].search([('user_id', '=', username)])
        userID = user.id
        print(userID)
        print(type)
        request.env['hrstore.product'].sudo().create({'pro_name': name, 'pro_price': price, 'pro_detail': detail,
                                                      'pro_type': type, 'state': state, 'pro_view': view, 'user_id': userID,
                                                      'pro_image': image})

        return request.render('HRStore.home')