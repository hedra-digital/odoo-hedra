# -*- coding: utf-8 -*-

from odoo import fields, models, _ , api
from odoo.exceptions import UserError
import requests
import json
import base64
import logging
_logger = logging.getLogger(__name__)


class Book_create_isbn(models.TransientModel):
    _name = "book.create.isbn"
    _description = "Search Book and Create Record"

    name = fields.Char("Title")
    is_search_book = fields.Boolean('Is Search Book')
    product_image = fields.Binary('Product Image')
    search_book =  fields.Char('Search Book with ISBN Code')
    full_title = fields.Char("Full Title")
    isbn = fields.Char("ISBN")
    isbn_13 = fields.Char("ISBN-13")
    edition = fields.Char("Edition")
    publish_date = fields.Char("Publish Date")
    binding = fields.Char("Binding")
    isbn_auther_ids = fields.Many2many('isbn.auther.publiser', string='Authers')
    isbn_publisher_id = fields.Many2one('isbn.auther.publiser','Publisher')

    @api.multi
    def search_book_isbn_code(self):
        headers = { 
           'Content-Type': 'application/json',  
           'X-API-Key': '1K6FGwYFAU6P9dISV11eM978nT3uqxnDuDSPHcTh'}
        url ="http://api.isbndb.com/books/"+self.search_book
        response = requests.get(url, headers=headers)
        books = json.loads(response.text).get('books') and json.loads(response.text).get('books')[0]
        isbn_auther_publiser_obj = self.env['isbn.auther.publiser']
        publiser_isbn = isbn_auther_publiser_obj.search([
                ('name','=',books.get('publisher')),
                ('is_publiser','=', True)
            ])

        self.isbn = books.get('isbn')
        self.isbn_13 = books.get('isbn13')
        self.name = books.get('title')
        self.edition = books.get('edition')
        self.binding = books.get('binding')
        self.publish_date = books.get('publish_date')
        self.full_title = books.get('title_long')
        for auther in books.get('authors'):
            auther_exist = isbn_auther_publiser_obj.search([
                    ('name','=',auther),
                    ('is_auther','=',True)
                ])
            if auther_exist:
                self.isbn_auther_ids = [(4,auther_exist.id)]
            else:
                self.isbn_auther_ids = [(0,0,{'name': auther, 'is_auther': True})]

        self.product_image = base64.b64encode(requests.get(books.get('image')).content)
        self.is_search_book = True
        if publiser_isbn:
            self.isbn_publisher_id = publiser_isbn.id
        else:
            self.isbn_publisher_id = isbn_auther_publiser_obj.create({
                'name': books.get('publisher'),
                'is_publiser': True})
        return {
            'name':_("Isbn Books"),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': False,
            'res_model': 'book.create.isbn',
            'res_id':self.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    def create_product_from_isbn_book(self):
        product_template = self.env['product.template']
        books = product_template.search([('isbn_13','=',self.isbn_13)])
        values = {
            'name': self.name,
            'description_sale': self.full_title,
            'image_medium' : self.product_image,
            'book_auther_ids' : [(6,0,self.isbn_auther_ids.ids)],
            'isbn': self.isbn,
            'isbn_13': self.isbn_13,
            'edition' : self.edition,
            'isbn_publisher_id' : self.isbn_publisher_id.id,
            'publish_date' : self.publish_date,
            'binding': self.binding
        }
        if books:
            books.write(values)
            _logger.warning('Book with isbn13 %s is updated', self.isbn_13)

        else:
            product_template.create(values)
            _logger.warning('Book with isbn13 %s is created', self.isbn_13)    

        
        return True    