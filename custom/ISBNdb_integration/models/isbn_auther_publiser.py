# -*- coding: utf-8 -*-

from odoo import fields, models, _ , api
from odoo.exceptions import UserError


class Isbn_auther_publiser(models.Model):
	_name ='isbn.auther.publiser'

	name = fields.Char("Name")
	is_auther = fields.Boolean("Is Auther")
	is_publiser = fields.Boolean("Is Publiser")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
