# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Import Sale Order Lines from Excel or CSV File',
    'version': '10.0.0.0',
    'summary': 'Easy to Import multiple sales order lines on Odoo by Using CSV/XLS file',
    'category': 'Sales',
    "price": 20,
    "currency": 'EUR',
    'description': """
	BrowseInfo developed a new odoo/OpenERP module apps.
	This module use for import bulk Sales Order lines from Excel file. Import Sales order lines from CSV or Excel file.
	Import Sales, Import Sale order line, Import Sale lines, Import SO Line. Sale Import, Add SO from Excel.Add Excel Sale order lines.Add CSV file.Import Sale data. Import excel file
	-
    """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    
    'depends': ['base','sale'],
    'data': [
    		  'import_order_lines_view.xml',
            ],
    'demo': [],
    'test': [],
    'installable':True,
    'auto_install':False,
    'application':True,
    "images":['static/description/banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
