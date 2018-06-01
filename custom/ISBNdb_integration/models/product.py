# -*- coding: utf-8 -*-

from odoo import fields, models, _ , api
from odoo.exceptions import UserError


class product(models.Model):
	_inherit='product.template'

	book_auther_ids = fields.Many2many('isbn.auther.publiser',string='Auther Name')
	isbn_publisher_id = fields.Many2one('isbn.auther.publiser','Publisher')
	publish_date = fields.Char("Publish Date")
	binding = fields.Char("Binding")
	isbn = fields.Char("ISBN")
	isbn_13 = fields.Char("ISBN-13")
	edition = fields.Char("Edition")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
