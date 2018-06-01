# -*- coding: utf-8 -*-

{
    'name': "Hedra",

    'summary': 'Estoque Consignado',

    'description': 'Módulo destinado ao controle de estoque do tipo consignado para a editora Hedra.',

    'author': "Rodrigo, Leonardo - SOLAP",
    
    'website': "http://www.solap.com.br/",
    
    'category': 'General',
    
    'version': '1.0',

    'depends': ['base', 'crm','stock','sale_management','stock_account','mail','account','account_invoicing','account_accountant',
                'account_bank_statement_import','account_bank_statement_import_csv','account_bank_statement_import_ofx','account_cancel','account_extension','account_reports',
                'analytic','auth_crypt','auth_signup','barcodes','base','base_automation','base_import','base_import_module','base_setup','br_account','br_account_einvoice',
                'br_bank_statement_import','br_base','br_coa','br_crm','br_crm_zip','br_data_account','br_data_account_product','br_data_base','br_product','br_sale','br_sale_stock',
                'br_stock_account','br_zip','bus','calendar_sms','contacts','currency_rate_live','decimal_precision','document','fetchmail','iap','import_order_lines','mail_push',
                'payment','payment_transfer','procurement_jit','product','resource','sale','sale_crm','sales_team','sale_stock','sms','utm','web','web_clearbit','web_diagram',
                'web_editor','web_enterprise','web_gantt','web_grid','web_kanban_gauge','web_mobile','web_planner','web_settings_dashboard','web_studio','web_tour','calendar',
                'portal','http_routing', 'br_nfe', 'br_nfse', 'br_nfse_paulistana', 'website_sale',
            ],

    'data': [
        'security/ir.model.access.csv',
        'views/res_view.xml',
        'views/sale_view.xml',
        'views/stock.xml',
        'views/import_wizard_product_adj.xml',
        'views/consignment_view.xml',
    ],
    'application':True,
    # only loaded in demonstration mode
    #'demo': [
        # 'demo.xml',
    #],
}
