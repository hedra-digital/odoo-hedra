from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from xmlrpc import client
from xmlrpc.client import ServerProxy as XMLServerProxy
import logging
import psycopg2
try:
    import erppeek
except :
    raise UserError(_('Library erppeek not installed Try: sudo pip install -U erppeek '))

class StockQuant(models.Model):
    _inherit = "stock.quant"

    sync = fields.Boolean('Sync') 


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    sync = fields.Boolean('Sync')


class DatabaseConnection(models.Model):
    _name ='database.sync'
 
    dbase_name = fields.Char('DB Name', required=True, )
    credential=fields.Boolean("Show/Hide Credentials Tab ")
    name=fields.Char('Root URL', required=True,)
    user=fields.Char('User Name', required=True, )
    password=fields.Char('Password', required=True, )
    database_server=fields.Boolean('Product Server')
    server_connected=fields.Boolean('Server Connected')
    sync_product=fields.Boolean('Sync Product')



    @api.multi
    def sync_city_id(self):
        count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if url:
            srv = 'http://localhost:8069'
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            state_obj = self.env['res.country.state']
            state_env = api.execute_kw(db, 1, pwd, 'res.country.state', 'search', [[]]) 
            for value in state_env:
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT name,code,country_id from res_country_state where id=%s'%(value))
                vals = cur.fetchall()[0]
                res = self.env['res.country.state'].search([('code','=',vals[1])])

                if res: 
                    logging.info("State already exists----------%s", vals[0])
                if not res:
                    val = {
                        'name':vals[0],
                        'code':vals[1],
                        'country_id':vals[2],
                          } 
                    logging.info("State Does not exists----------%s", val)
                    state_id = state_obj.create(val)
                    count +=1  
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
        else :
            message = 'Connection Error: Unbale to connect to database '
            temp_id = self.env['wizard.message'].create({'text':message})
            return {
                    'name':_("Test Result"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'wizard.message',
                    'res_id': temp_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                   }
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }




    @api.multi
    def sync_state_id(self):
        count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if url:
            srv = 'http://localhost:8069'
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            state_obj = self.env['res.country.state']
            state_env = api.execute_kw(db, 1, pwd, 'res.country.state', 'search', [[]]) 
            for value in state_env:
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT name,code,country_id from res_country_state where id=%s'%(value))
                vals = cur.fetchall()[0]
                res = self.env['res.country.state'].search([('code','=',vals[1])])
                if res: 
                    logging.info("State already exists----------%s", vals[0])
                if not res:
                    val = {
                        'name':vals[0],
                        'code':vals[1],
                        'country_id':vals[2],
                          } 
                    logging.info("State Does not exists----------%s", val)
                    state_id = state_obj.create(val)
                    count +=1  
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
        else :
            message = 'Connection Error: Unbale to connect to database '
            temp_id = self.env['wizard.message'].create({'text':message})
            return {
                    'name':_("Test Result"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'wizard.message',
                    'res_id': temp_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                   }
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }



    @api.multi
    def sync_partner_address(self):
        count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if True:
            srv = 'http://localhost:8069'
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            #categ_env = self.env['res.partner.category'].search([])
            #for value in categ_env: 
            #    res = api.execute_kw(db, 1, pwd, 'res.partner.category', 'search', [[('name','=',value.name)]]) 
            #    if not res:
            #        val = {
            #            'name':value.name,
            #              } 
            #        categ_id = api.execute_kw(db, 1, pwd, 'res.partner.category', 'create', [val])
            partner_env = api.execute_kw(db, 1, pwd, 'res.partner', 'search', [[('parent_id','!=',False)]])
            state_obj = self.env['res.country.state']
            country_obj = self.env['res.country']
            lang_obj = self.env['res.lang']
            city_obj = self.env['res.state.city']
            partner_obj = self.env['res.partner']
            print ("Total record found =====>",len(partner_env))
            for value in partner_env: 
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT name,number,is_company,street,parent_id,comment,active,city,type,partner_share,district,cnpj_cpf,inscr_mun,suframa, inscr_est, street2,website,phone,mobile,fax,email,customer,supplier,zip,state_id,country_id,city_id,lang from res_partner where id=%s'%(value))
                vals = cur.fetchall()[0]
                res = self.env['res.partner'].search([('name','=',vals[0]),('cnpj_cpf','=',vals[11])])
                parent_id = None
                if vals[4]:
                    conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                    cur = conn.cursor()
                    cur.execute('SELECT name,cnpj_cpf from res_partner where id=%s'%(vals[4]))
                    parent_name = cur.fetchall()[0]
                    print ("FDDFFFFFFFFF+=======",parent_name)
                    parent_id = self.env['res.partner'].search([('name','=',parent_name[0]),('cnpj_cpf','=',parent_name[1])])
                    if parent_id:
                        parent_id = parent_id.ids[0]
                    else:
                        continue
                        #raise UserError(_('parent_name Doed not exixts '))
                res = self.env['res.partner'].search([('name','=',vals[0]),('cnpj_cpf','=',vals[11])])
                print ("Final Feched Partner Data =====",vals)
                if not res:
                    state_id = None,
                    country_id =None,
                    city_id = None
                    if vals[24]:
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, code from res_country_state where id=%s'%(vals[24]))
                        state_vals = cur.fetchall()[0]
                        print("State Searching for =======",state_vals[0])
                        state_id = state_obj.search([('code','=',state_vals[1])])
                        if not state_id:
                            raise UserError(_('State Doed not exixts '))
                        else:
                            state_id = state_id.ids[0] 
                        print("state_id found for =======",state_id)
                    if vals[25]:
                        print ("country ID ====",vals[25])
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, code from res_country where id=%s'%(vals[25]))
                        country_vals = cur.fetchall()[0]
                        print("Country Searching for =======",country_vals[0],country_vals[1])
                        country_id = country_obj.search([('code','=',country_vals[1])])
                        if not country_id:
                            raise UserError(_('country_vals Doed not exixts '))
                        else:
                            country_id = country_id.ids[0] 
                        print("country_id found for =======",country_id)
                    if vals[26]:
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, ibge_code from res_state_city where id=%s'%(vals[26]))
                        city_vals = cur.fetchall()[0]
                        print("City Searching for =======",city_vals[0])
                        city_id = city_obj.search([('ibge_code','=',city_vals[1])])
                        if not city_id:
                            raise UserError(_('city Doed not exixts '))
                        else:
                            city_id = city_id.ids[0] 
                        print("city_id found for =======",city_id)
                    val = {
                          'name':vals[0],
                          'number':vals[1],
                          'is_company':vals[2],
                          'street':vals[3],
                          'parent_id':parent_id,
                          'comment':vals[5],
                          'active':vals[6],
                          'city':vals[7],
                          'type':vals[8],
                          'partner_share':vals[9],
                          'district':vals[10],
                          'cnpj_cpf':vals[11],
                          'inscr_mun':vals[12],
                          'suframa':vals[13],
                          'inscr_est':vals[14],
                          'street2':vals[15],
                          'website':vals[16],
                          'phone':vals[17],
                          'mobile':vals[18],
                          'email':vals[20],
                          'customer':vals[21],
                          'supplier':vals[22],
                          'zip':vals[23], 
                          'state_id':state_id,
                          'country_id':country_id,
                          'city_id':city_id
                          }     
                    count = count + 1
                    if count > 100:
                        break
                    print ("Final data to create -=====",val)
                    res_parent = partner_obj.create(val)
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
        else :
            message = 'Connection Error: Unbale to connect to database '
            temp_id = self.env['wizard.message'].create({'text':message})
            return {
                    'name':_("Test Result"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'wizard.message',
                    'res_id': temp_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                   }
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }


    @api.multi
    def sync_invoice(self):
        count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if True:
            srv = 'http://localhost:8069'
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            invoices_env = []
            conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
            cur = conn.cursor()
            cur.execute("SELECT id from account_invoice where state='paid'")
            invoices = cur.fetchall() 
            partner_obj = self.env['res.partner']
            invoice_obj = self.env['account.invoice']
            product_obj = self.env['product.product']
            print ("Total record found =====>",len(invoices))
            for value in invoices: 
                print("Invoice Id found in list====",value)
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT number,partner_id,payment_term_id,date_invoice,account_id from account_invoice where id=%s'%(value))
                vals = cur.fetchall()[0]
                res = invoice_obj.search([('name','=',vals[0])])
                if vals[1]:
                    conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                    cur = conn.cursor()
                    cur.execute('SELECT name,email,cnpj_cpf from res_partner where id=%s'%(vals[1]))
                    partner_vals = cur.fetchall()[0]
                    partner_id = partner_obj.search([('name','=',partner_vals[0]),('email','=',partner_vals[1]),('cnpj_cpf','=',partner_vals[2])]) 
                    if not partner_id:
                        print("partner_vals not found for =======",partner_vals)
                        raise UserError(_('partner_vals Doed not exixts '))
                    else:
                        partner_id = partner_id.ids[0] 
                print ("Final Feched Invoice Data =====",vals)
                if not res:
                    order_lines = []
                    conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                    cur = conn.cursor()
                    cur.execute('SELECT product_id,quantity,price_unit,discount,name,account_id from account_invoice_line where invoice_id=%s'%(value))
                    invoice_line_vals = cur.fetchall()
                    print ("invoice_line_vals ===== found ====",invoice_line_vals)                    
                    for line in invoice_line_vals:
                        print("line_vals found =======",line)
                        account_id = None
                        if line[5]:
                            conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                            cur = conn.cursor() 
                            cur.execute('SELECT name, code from account_account where id=%s'%(line[5]))
                            account_id_val = cur.fetchall()[0]
                            account_id = self.env['account.account'].search([('code','=',account_id_val[1])])
                            if not account_id:
                                print("account_id not found for =======",account_id_val) 
                        if line:
                            conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                            cur = conn.cursor()
                            cur.execute('SELECT product_tmpl_id,default_code from product_product where id=%s'%(line[0]))
                            product_templ_id = cur.fetchall()[0][0]
                            conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                            cur = conn.cursor()
                            cur.execute('SELECT name from product_template where id=%s'%(product_templ_id))
                            product_data = cur.fetchall()
                            print ("Product Data found====",product_data)
                            product_id = product_obj.search([('name','=',product_data[0][0])])
                            if not product_id:
                                print("product_data not found for =======",product_data)
                                continue
                                raise UserError(_('product_data Doed not exixts '))
                            else:
                                product_id = product_id.ids[0]
                            pro_val = {
                              'product_id':product_id,
                              'quantity':line[1],
                              'price_unit':line[2], 
                              'discount':line[3],
                              'name': line[4],
                              'account_id': 135,
                                  }
                            print("pto_val data =========>",pro_val)
                            order_lines.append((0,0,pro_val))
                    val = {
                          'name':vals[0],
                          'partner_id':partner_id,
                          'date_invoice':vals[3],
                          'invoice_line_ids':order_lines,
                          'state':'cancel'
                          }     
                    count = count + 1
                    if count > 500:
                        break
                    print ("Final data to create -=====",val)
                    res_parent = invoice_obj.create(val)
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
        else :
            message = 'Connection Error: Unbale to connect to database '
            temp_id = self.env['wizard.message'].create({'text':message})
            return {
                    'name':_("Test Result"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'wizard.message',
                    'res_id': temp_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                   }
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }

    @api.multi
    def sync_partner_mapping(self):
        count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if True:
            srv = 'http://localhost:8069'
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            #categ_env = self.env['res.partner.category'].search([])
            #for value in categ_env: 
            #    res = api.execute_kw(db, 1, pwd, 'res.partner.category', 'search', [[('name','=',value.name)]]) 
            #    if not res:
            #        val = {
            #            'name':value.name,
            #              } 
            #        categ_id = api.execute_kw(db, 1, pwd, 'res.partner.category', 'create', [val])
            partner_env = api.execute_kw(db, 1, pwd, 'res.partner', 'search', [[('parent_id','=',False),('active','=',False)]])
            state_obj = self.env['res.country.state']
            country_obj = self.env['res.country']
            lang_obj = self.env['res.lang']
            city_obj = self.env['res.state.city']
            partner_obj = self.env['res.partner']
            print ("Total record found =====>",partner_env)
            for value in partner_env: 
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT name,number,is_company,street,parent_id,comment,active,city,type,partner_share,district,cnpj_cpf,inscr_mun,suframa, inscr_est, street2,website,phone,mobile,fax,email,customer,supplier,zip,state_id,country_id,city_id,lang from res_partner where id=%s'%(value))
                vals = cur.fetchall()[0]
                res = self.env['res.partner'].search([('name','=',vals[0]),('cnpj_cpf','=',vals[11])])
                print ("Final Feched Partner Data =====",vals)
                if not res:
                    state_id = None,
                    country_id =None,
                    city_id = None
                    if vals[24]:
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, code from res_country_state where id=%s'%(vals[24]))
                        state_vals = cur.fetchall()[0]
                        print("State Searching for =======",state_vals[0])
                        state_id = state_obj.search([('code','=',state_vals[1])])
                        if not state_id:
                            raise UserError(_('State Doed not exixts '))
                        else:
                            state_id = state_id.ids[0] 
                        print("state_id found for =======",state_id)
                    if vals[25]:
                        print ("country ID ====",vals[25])
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, code from res_country where id=%s'%(vals[25]))
                        country_vals = cur.fetchall()[0]
                        print("Country Searching for =======",country_vals[0],country_vals[1])
                        country_id = country_obj.search([('code','=',country_vals[1])])
                        if not country_id:
                            raise UserError(_('country_vals Doed not exixts '))
                        else:
                            country_id = country_id.ids[0] 
                        print("country_id found for =======",country_id)
                    if vals[26]:
                        conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                        cur = conn.cursor()
                        cur.execute('SELECT name, ibge_code from res_state_city where id=%s'%(vals[26]))
                        city_vals = cur.fetchall()[0]
                        print("City Searching for =======",city_vals[0])
                        city_id = city_obj.search([('ibge_code','=',city_vals[1])])
                        if not city_id:
                            raise UserError(_('city Doed not exixts '))
                        else:
                            city_id = city_id.ids[0] 
                        print("city_id found for =======",city_id)
                    val = {
                          'name':vals[0],
                          'number':vals[1],
                          'is_company':vals[2],
                          'street':vals[3],
                          'parent_id':vals[4],
                          'comment':vals[5],
                          'active':vals[6],
                          'city':vals[7],
                          'type':vals[8],
                          'partner_share':vals[9],
                          'district':vals[10],
                          'cnpj_cpf':vals[11],
                          'inscr_mun':vals[12],
                          'suframa':vals[13],
                          'inscr_est':vals[14],
                          'street2':vals[15],
                          'website':vals[16],
                          'phone':vals[17],
                          'mobile':vals[18],
                          'email':vals[20],
                          'customer':vals[21],
                          'supplier':vals[22],
                          'zip':vals[23], 
                          'state_id':state_id,
                          'country_id':country_id,
                          'city_id':city_id
                          }     
                    count = count + 1
                    if count > 500:
                        break
                    print ("Final data to create -=====",val)
                    res_parent = partner_obj.create(val)
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
        else :
            message = 'Connection Error: Unbale to connect to database '
            temp_id = self.env['wizard.message'].create({'text':message})
            return {
                    'name':_("Test Result"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'wizard.message',
                    'res_id': temp_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                   }
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }





    @api.multi
    def sync_product_mapping(self):
        count=0
        un_count=0
        url=self.name
        user=self.user
        pwd=self.password
        db=self.dbase_name
        if True:
            srv = 'http://localhost:8069' 
            api = XMLServerProxy('%s/xmlrpc/2/object' % srv)
            product_env = api.execute_kw(db, 1, pwd, 'product.template', 'search', [[('active','=',False)]])
            print ("Total Products found =====================",len(product_env))
            product_obj = self.env['product.template']
            for value_id in product_env:
                #count += 1
                #if count > 25:
                #    break
                conn = psycopg2.connect(host="localhost",database=self.dbase_name, user='megh', password='megh')
                cur = conn.cursor()
                cur.execute('SELECT name,type,default_code,sale_ok,purchase_ok,list_price,fiscal_classification_id from product_template where id=%s'%(value_id))
                vals = cur.fetchall()[0]
                pro_name = vals[0]
                if ']' in pro_name:
                    pro_name = pro_name.split(']')
                    pro_name = pro_name[1][1:len(pro_name[1])]
                print (vals)
                print ("\n")
                print ("Total Products ID =====================",value_id)
                res = self.env['product.template'].search([('name','=',pro_name),('default_code','=',vals[2])])
                print ("Praveen=====================",vals)
                if not res:
                    val = {
                        'name':pro_name,
                        'default_code':vals[2],
                        'sale_ok':vals[3],
                        'purchase_ok':vals[4],
                        'type':vals[1],
                        'list_price':vals[5],
                        'fiscal_classification':vals[6]
                          }
                    #state_id = api.execute_kw(db, 1, pwd, 'product.product', 'write', [res, val])
                    product_id = product_obj.create(val)
                    count = count + 1
                else :
                    un_count += 1
            message="Total product mapped : "+str(count)        
            temp_id = self.env['wizard.message'].create({'text':message})
            #print "Product Not Created ==================>",un_count\
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
                }





    @api.multi
    def test_connection(self):
        for val in self:
            message="Test successful...you can proceed now."
            url=self.name
            user=self.user
            pwd=self.password
            db=self.dbase_name
            try:
                common = XMLServerProxy('%s/xmlrpc/2/common' % url)
                self.write({'server_connected':True})
                uid = common.authenticate(db, user, pwd, {})
                temp_id = self.env['wizard.message'].create({'text':message})
            except Exception:
                message = 'Connection Error: Server cannot be connected Invalid Credentials!!'
                temp_id = self.env['wizard.message'].create({'text':message})
                return {
                        'name':_("Test Result"),
                        'view_mode': 'form',
                        'view_id': False,
                        'view_type': 'form',
                        'res_model': 'wizard.message',
                        'res_id': temp_id.id,
                        'type': 'ir.actions.act_window',
                        'nodestroy': True,
                        'target': 'new',
                        'domain': '[]',
                       }
                 
        return {
                'name':_("Test Result"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wizard.message',
                'res_id': temp_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
               }

