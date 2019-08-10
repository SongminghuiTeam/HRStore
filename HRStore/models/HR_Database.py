from odoo import models, fields


class HRUser(models.Model):
    _name = 'hrstore.user'
    _description = 'HRStore User'

    user_id = fields.Char('账号', required=True)
    password = fields.Char('密码', required=True)
    user_type = fields.Char('用户类型')


class HRCommonUser(models.Model):
    _name = 'hrstore.commonuser'
    _description = 'HRStore CommonUser'

    username = fields.Char('昵称')
    telephone = fields.Char('电话')
    address = fields.Text('地址')
    user_id = fields.Char('账号', required=True)


class HRShop(models.Model):
    _name = 'hrstore.shop'
    _description = 'HRStore Shop'

    shopname = fields.Char('名称')
    telephone = fields.Char('电话')
    address = fields.Text('地址')

    user_id = fields.Char('账号', required=True)


class HRProduct(models.Model):
    _name = 'hrstore.product'
    _description = 'HRStore Product'

    pro_name = fields.Char('产品名称')
    pro_image = fields.Binary(string='图片')
    pro_price = fields.Float('价格', (10, 2))
    pro_detail = fields.Text('商品详情')
    pro_type = fields.Char('产品类型')

    user_id = fields.Many2one(
        'res.partner',
        string='商家ID',
        ondelete='set null',
        context={},
        domain=[],
    )


class HROrder(models.Model):
    _name = 'hrstore.order'
    _description = 'HRStore Order'

    order_time = fields.Datetime('下单时间')
    order_state = fields.Char('订单状态')
    order_price = fields.Float('价格', (10, 2))

    user_id = fields.Many2one(
        'res.partner',
        string='用户ID',
        ondelete='set null',
        context={},
        domain=[],
    )

    pro_id = fields.Char('产品ID')


class HRCart(models.Model):
    _name = 'hrstore.cart'
    _description = 'HRStore Cart'

    cart_num = fields.Integer('数量')

    user_id = fields.Char('账号', required=True)

    pro_id = fields.One2many(
        'hrstore.product',
        'id',
        string='产品ID'
    )


class HRComment(models.Model):
    _name = 'hrstore.comment'
    _description = 'HRStore Comment'

    content = fields.Text('内容')
    time = fields.Datetime('评论时间')

    user_id = fields.Many2one(
        'res.partner',
        string='用户ID',
        ondelete='set null',
        context={},
        domain=[],
    )

    pro_id = fields.Many2one(
        'res.partner',
        string='产品ID',
        ondelete='set null',
        context={},
        domain=[],
    )







