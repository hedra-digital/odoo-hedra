# -*- coding: utf-8 -*-

from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo import api, fields, models,_
from odoo.tools.float_utils import float_compare
from iugu import Invoice

import logging
import pprint
import os
import datetime

_logger = logging.getLogger(__name__)

os.environ["IUGU_API_TOKEN"] = "SEU_IUGU_API_TOKEN"

class IuguBoleto(models.Model, Invoice):
    _inherit = 'payment.acquirer'


    provider = fields.Selection(selection_add=[('iugu', 'Boleto Bancário')])

    # def _get_providers(self, cr, uid, context=None):
    #     providers = super(IuguBoleto, self)._get_providers(cr, uid, context=context)
    #     providers.append(['iugu', _('Boleto Bancário')])
    #     return providers

    @api.multi
    def iugu_get_form_action_url(self):
        return '/payment/iugu/feedback'

    @api.multi    
    def iugu_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        iugu_tx_values = dict(values)
        iugu_tx_values.update({
            'cmd': '_xclick',
            'business': self.paypal_email_account,
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'handling': '%.2f' % iugu_tx_values.pop('fees', 0.0) if self.fees_active else False,
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
        })
        return iugu_tx_values    

    @api.model    
    def _create_iugu_invoice(self, data):
        nome = data.get('name')
        item_name = data.get('item_name')
        email = data.get('email')
        address = data.get('address')
        city = data.get('city')
        zip = data.get('zip')
        country = data.get('country')
        item_number = data.get('item_number')
        amount = float(data.get('amount', '0'))
        today = datetime.date.today()

        dados_invoice = {
            'email': email,
            'due_date': today.strftime('%d/%m/%Y'),
            'items': [{
                      'description': item_name,
                      'quantity': item_number,
                      'price_cents': amount * 100
                      }],
            'payer': {
                'name': nome,
                'address': {
                    'street': address,
                    'city': city,
                    'country': country,
                    'zip_cod': zip
                }
            }
        }

        invoice = Invoice()
        result = invoice.create(dados_invoice)
        _logger.info(pprint.pformat(result))