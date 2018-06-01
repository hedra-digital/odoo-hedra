# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
import datetime


class sale_order(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection([('sale','Venda Regular'),('con_order','Envio de Consignação'),
    ('con_sale','Acerto de Consignação')], string = "Tipo de Venda/Pedido", default='sale', required=True)

    #date_time = fields.Datetime('Data e Hora')
    
    @api.onchange('order_type', 'partner_id')
    def onchange_order_type_partner(self):
        print("##### onchange_order_type_partner [START] #####")
        
        result = {}
        
        count = 0
        
        for each_line in self.order_line:
            count += 1
        
        if count > 0:
            result['warning'] = {'title': "Aviso!",'message': "Alterações no Cliente ou Tipo de Venda/Pedido após inserir um produto, poderá causar inconsistência."}
        
        print("##### onchange_order_type_partner [END] #####")
        
        return result
    
    @api.onchange('order_type')
    def onchange_order_type(self):
        print("##### onchange_order_type [START] #####")
        
        result = {}
        
        if self.order_type and self.order_type != 'sale':
            result['domain'] = {'partner_id':[('allow_consignment','=',True),('customer','=',True)]}
            
            if self.partner_id:
                partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
                
                if not partner['allow_consignment']:
                    result['value'] = {'partner_id':False}
                    
                    result['warning'] = {'title': "Aviso!",'message': "Este Cliente não permite operações de consignação."}
                    
        elif self.order_type and self.order_type == 'sale':
            result['domain'] = {'partner_id':[('customer','=',True)]}
        
        print("##### onchange_order_type [END] #####")
        
        return result

    @api.multi
    def action_confirm(self):
        if self.order_type == 'con_sale':
            if len(self.order_line) < 1:
                raise Warning("Adicione um ou mais produtos para confirmar o Acerto de Consignação.")
                return False
            else:
                estoque = self.env['stock.quant'].search([('location_id.id', '=', self.partner_id.consignee_location_id.id)])
                
                flag = False
                excluir = []
                log = ""
                for item in self.order_line:
                    print(item.product_id.id)
                    for produto in estoque:
                        if item.product_id == produto.product_id:
                            qtde_estoque = produto.quantity
                            qtde_acerto = item.product_uom_qty
                            qtde_atual = qtde_estoque - qtde_acerto
                            
                            if qtde_atual >= 0:
                                produto.write({'quantity': qtde_atual})
                            else:
                                log = log + "Produto: %s - Qtde: %d<br>" % (produto.product_id.name, int(qtde_atual))
                                excluir.append(produto)
                                flag = True

                if bool(excluir): 
                    for registro in excluir:
                        registro.unlink()

                if flag:
                    self.create_message(log)                            

                self.write({'state':'sale', 'confirmation_date':datetime.datetime.now()})
                
                return True
        else:
            if len(self.order_line) < 1:
                raise Warning("Adicione um ou mais produtos para confirmar o Acerto de Consignação.")
            else:
                return super(sale_order, self).action_confirm()
    
    @api.multi
    def action_view_sale_consignment_products(self):
        imd = self.env['ir.model.data']
        
        list_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_tree')        
        form_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_form')        
        action = self.env.ref('hedra.consignee_open_quants').read()[0]        
        action['views'] = [[list_view_id, 'tree'], [form_view_id, 'form']]        
        action['context'] = {'search_default_internal_loc': 1, 'search_default_productgroup': 1}                
        action['domain'] = "[('location_id','=',%s)]" % self.partner_id.consignee_location_id.id        
        action['target'] = "new"

        return action

    #Opção 2 caso o envio da mensagem pelo canal dê errado
    @api.multi
    def teste_email(self):
        print("Teste")
        email = self.env['mail.mail'].create(
            {'subject' : 'Aviso! Acerto de Consignação x negativou o estoque',
             'email_from' : 'projetos@solap.com.br',
             'email_to' : 'projetos@solap.com.br',
             'body_html' : 'Aqui vai o aviso de que o estoque negativou para o acerto x',
             'message_type' : 'email'
            }
        )
        print(email.id)
        email.send()

    @api.multi
    def create_channel(self):
        mail_channel = self.env['mail.channel'].create(
                {'name' : 'Erros de Consignação',
                 'public' : 'public'
                }
            )
        self.env['mail.channel.partner'].create(
                {'partner_id' : self.env.user.partner_id.id,
                 'channel_id' : mail_channel.id
                }
            )

        return mail_channel

    @api.multi
    def create_message(self, log):
        record_name = 'Erros de Consignação'
        channel =  self.env['mail.channel'].search([('name', '=', record_name)])
        print(channel, bool(channel))

        if not bool(channel):
            print("Criando um canal")
            channel = self.create_channel()
            print(channel)
            
        date = datetime.datetime.now()
        email_from = self.env.user.partner_id.email
        author_id = self.env.user.partner_id.id
        model = 'mail.channel'
        res_id = channel.id
        message_type = 'comment'

        body = 'A venda de Ajuste de Consignação %s gerou estoque negativo para o(s) seguinte(s) produto(s):<br>' % self.name + log

        vals = {'date' : date, 
                'email_from' : email_from, 
                'author_id' : author_id, 
                'record_name' : record_name,
                'model' : model,
                'res_id' : res_id,
                'message_type' : message_type,
                'channel_ids' : [(4, res_id)],
                'body' : body
               }

        message = self.env['mail.message'].create(vals)
        if message:
            print("Mensagem enviada com sucesso para o canal -", message)
        
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    consignment_stock = fields.Float(string='Estoque em Consignação', compute='_compute_consignment_stock', store=True)
    
    @api.one
    @api.depends('product_id')
    def _compute_consignment_stock(self):
        print ("##### _compute_consignment_stock [START] #####")
        
        if not self.product_id:
            return
        
        consignent_location = self.order_id.partner_id.consignee_location_id
        
        if not consignent_location:
            return False
        
        consignment_quants = self.env['stock.quant'].search([('location_id','=',consignent_location.id),
            ('product_id','=', self.product_id.id)])
        
        product_qty = 0
        
        for each_quant in consignment_quants:
            product_qty += each_quant.quantity

        consignment_stock = product_qty
        
    print ("##### _compute_consignment_stock [END] #####")

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            if self.order_id.order_type != 'sale' and self.product_id.product_tmpl_id.type != 'product':
                result = {}
        
                result['value'] = {'product_id':False, 'name':False, 'product_uom_qty':1, 'price_unit':False, 'tax_id':False, 'price_subtotal':False}
                
                result['warning'] = {'title': "Aviso!",'message': "Este Tipo de Produto não é permitido em operações de consignação."}
                
                return result
            
            consignment_quants = self.env['stock.quant'].search([('location_id','=',self.order_id.partner_id.consignee_location_id.id),
                ('product_id','=', self.product_id.id)])
            
            product_qty = 0
            
            for each_quant in consignment_quants:
                product_qty += each_quant.quantity

            consignment_stock = product_qty
            
            self.consignment_stock = consignment_stock
    
    @api.onchange('product_uom_qty', 'product_id')
    def _onchange_consignment_stock(self):
        if self.product_id and self.order_id.order_type == 'con_sale':
            
            consignment_quants = self.env['stock.quant'].search([('location_id','=',self.order_id.partner_id.consignee_location_id.id),
                ('product_id','=', self.product_id.id)])
            
            product_qty = 0
            
            for each_quant in consignment_quants:
                product_qty += each_quant.quantity

            consignment_stock = product_qty
                
            if self.product_uom_qty > consignment_stock:
                return {
                    'warning': {
                        'title': "Aviso!",
                        'message': "Esta Venda Consignada irá negativar o estoque de consignação deste produto.",
                    },
                }
        