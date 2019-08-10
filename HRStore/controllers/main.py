# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Hello(http.Controller):
    @http.route('/helloworld',auth="public")
    def helloworld(self, **kwargs):
        return request.render('HRStore.helloworld')

