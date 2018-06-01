#!/usr/bin/env python
# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    "name": "Isbn Integration",
    "version": "1.0",
    "author": "",
    "website": "exmaple.com",
    "category": "Extra Tools",
    "depends": ['sale', 'product'],
    "summary": "Isbn Integration",
    "description": """
        Isbn Integration
    """,
    "data": [
        'security/ir.model.access.csv',
        'wizard/book_create_isbn_view.xml',
        'view/product_views.xml'
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'auto_install': False,
    'application': False,
    'images': [],
    'license': 'Other proprietary',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
