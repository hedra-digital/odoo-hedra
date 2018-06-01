# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    @api.constrains('ean13')
    def _check_seats_limit(self):
        all_eans = self.search_read([('id','!=', self.id)],['ean13'])
        if self.ean13 and self.ean13 in [each['ean13'] for each in all_eans]:
            raise Warning(_('Este EAN já está em uso.'))

    ean13 = fields.Char('EAN13 Barcode', type='char')
    author_id = fields.Many2one('res.partner', 'Autor', domain=[('is_author','=',True)])
    pages = fields.Integer('Páginas')

    @api.multi
    @api.depends('product_variant_ids.sales_count')
    def _sales_count(self):
        super(product_template, self)._sales_count()

        cons_sale_list = self.env['sale.order'].search([('order_type','=','con_order')])
        
        produto_cons_qty = 0
        
        for pedido in cons_sale_list:
            for produto in pedido.order_line:

                if produto.product_id.product_tmpl_id.id == self.id:
                    produto_cons_qty += produto.product_uom_qty

        self.sales_count -= produto_cons_qty
