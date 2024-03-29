from odoo import models, fields, api


# 梁晓珂 计科162 161002221

class HRUser(models.Model):
    _name = 'hrstore.user'
    _description = 'HRStore User'
    _rec_name = 'user_id'

    user_id = fields.Char('账号', required=True)
    password = fields.Char('密码', required=True)
    user_type = fields.Selection(string='用户类型', selection=[('0', '管理员'), ('1', '普通用户'), ('2', '供应商')], default='1')


class HRCommonUser(models.Model):
    _name = 'hrstore.commonuser'
    _description = 'HRStore CommonUser'

    user_image = fields.Binary(string='头像', attachment=True)
    username = fields.Char('昵称')
    telephone = fields.Char('电话')
    address = fields.Text('地址')
    user_id = fields.Char('账号', required=True)


class HRAddress(models.Model):
    _name = 'hrstore.address'
    _description = 'HRStore Address'

    province = fields.Char('省')
    city = fields.Char('市')
    block = fields.Char('区')
    street = fields.Char('街道')
    details = fields.Char('详细地址')
    receiver_name = fields.Char('收货人姓名')
    receiver_tel = fields.Char('收货人电话')

    user_id = fields.Many2one(
        'hrstore.commonuser',
        string='普通用户',
        ondelete='set null',
    )


class HRShop(models.Model):
    _name = 'hrstore.shop'
    _description = 'HRStore Shop'
    _rec_name = 'shopname'

    user_image = fields.Binary(string='头像', attachment=True)
    shopname = fields.Char('名称')
    telephone = fields.Char('电话')
    address = fields.Text('地址')

    user_id = fields.Char('账号', required=True)


class HRProduct(models.Model):
    _name = 'hrstore.product'
    _description = 'HRStore Product'
    _order = 'pro_view desc'

    pro_name = fields.Char('产品名称')
    pro_image = fields.Binary(string='图片', attachment=True)
    pro_price = fields.Float('价格', (10, 2))
    pro_detail = fields.Text('商品详情')
    pro_type = fields.Selection(string='产品类型', selection=[('1', '活动策划'), ('2', '培训产品'), ('3', '精美商品'), ('4', '法律服务')],
                                default='0')
    state = fields.Selection(string='产品状态', selection=[('0', '待审核'), ('1', '已发布')], default='0')
    pro_view = fields.Integer(default=0, string='访问量')
    user_id = fields.Many2one(
        'hrstore.shop',
        string='供应商',
        ondelete='set null',
    )

    @api.multi
    def update_state(self):
        self.state = '1'


class HROrder(models.Model):
    _name = 'hrstore.order'
    _description = 'HRStore Order'

    order_time = fields.Datetime('下单时间')
    state = fields.Selection(string='订单状态', selection=[('0', '待处理'), ('1', '待付款'), ('2', '已通过')], default='0')
    order_price = fields.Float('价格', (10, 2))
    address_id = fields.Integer('收货地址')

    user_id = fields.Many2one(
        'hrstore.commonuser',
        string='用户ID',
        ondelete='set null',
    )

    # pro_id = fields.Char('产品ID')
    pro_id = fields.Many2one(
        'hrstore.product',
        string='产品ID',
        ondelete='set null',
    )


class HRCart(models.Model):
    _name = 'hrstore.cart'
    _description = 'HRStore Cart'

    cart_num = fields.Integer('数量', default=1)

    user_id = fields.Char('账号', required=True)

    pro_id = fields.Integer('产品id')


class HRComment(models.Model):
    _name = 'hrstore.comment'
    _description = 'HRStore Comment'

    content = fields.Text('内容')
    username = fields.Char('用户昵称')

    user_id = fields.Many2one(
        'hrstore.commonuser',
        string='用户ID',
        ondelete='set null',
    )

    order_id = fields.Many2one(
        'hrstore.order',
        string='产品ID',
        ondelete='set null',
    )


class HRForum(models.Model):
    _name = 'hrstore.forum'
    _description = 'HRStore Forum'
    _order = 'id desc'
    title = fields.Text('标题')
    content = fields.Text('内容')
    username = fields.Char('昵称')
    label = fields.Selection(string='标签',
                             selection=[('1', '公告'), ('2', '人员招聘'), ('3', '求职'), ('4', '我要提问'), ('5', '其他')],
                             default='1')

    user_id = fields.Many2one(
        'hrstore.user',
        string='用户ID',
        ondelete='set null',
    )


class HRAd(models.Model):
    _name = 'hrstore.ad'
    _description = 'HRStore Ad'

    title = fields.Text('标题')
    image = fields.Binary(string='图片', attachment=True)
    text = fields.Text('链接')