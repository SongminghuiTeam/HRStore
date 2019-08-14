from odoo import models, fields, api


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


class HRShop(models.Model):
    _name = 'hrstore.shop'
    _description = 'HRStore Shop'

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
    pro_type = fields.Selection(string='产品类型', selection=[('1', '活动策划'), ('2', '培训产品'), ('3', '精美商品'), ('4', '法律服务')], default='0')
    state = fields.Selection(string='产品状态', selection=[('0', '待审核'), ('1', '已发布')], default='0')
    pro_view = fields.Integer(default=0, string='访问量')
    user_id = fields.Many2one(
        'hrstore.user',
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
    state = fields.Selection(string='订单状态', selection=[('0', '待处理'), ('1', '已处理')], default='0')
    order_price = fields.Float('价格', (10, 2))

    user_id = fields.Many2one(
        'hrstore.user',
        string='用户ID',
        ondelete='set null',
    )

    pro_id = fields.Char('产品ID')


class HRCart(models.Model):
    _name = 'hrstore.cart'
    _description = 'HRStore Cart'

    cart_num = fields.Integer('数量',default=1)

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
        'hrstore.user',
        string='用户ID',
        ondelete='set null',
    )

    pro_id = fields.Many2one(
        'hrstore.product',
        string='产品ID',
        ondelete='set null',
    )







