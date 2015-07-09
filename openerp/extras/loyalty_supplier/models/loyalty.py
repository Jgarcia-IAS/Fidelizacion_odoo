# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE Johan Alejandro Olano (<http:http://www.ias.com.co).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.osv import orm, fields
from datetime import time, datetime
from openerp import SUPERUSER_ID


class loyalty_supplier (osv.osv):
    _name = "loyalty.supplier"
    _description = "Fidelizacion"

    def _calculate_points(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
            res[r.id] = + r.product_id.list_price
        return res

    _columns = {

        'name': fields.char(),
        'partner_id': fields.many2one('res.partner', 'Documento Cliente'),
        'product_id': fields.many2one('product.template', 'Producto', ),
        'sale_date': fields.date('Fecha de Venta'),
        'sale_arch': fields.date("Fecha De Carga del Archivo"),
        'puntos': fields.function(_calculate_points, "puntos", digits = (6,0),  store=True),
        'sale_order_id':fields.many2one('sale.order.line')


    }

    _defaults = {
        'sale_arch': datetime.now().strftime('%Y-%m-%d'),
        }


class res_partner (osv.osv):
    _inherit = 'res.partner'

    def get_restant_points(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for i in records:
            cr.execute("""  select coalesce(p - coalesce(price_nega,0),0)  as x
                        from (select sum(coalesce(puntos,0)) as p, partner_id from loyalty_supplier group by partner_id ) as  tabla1
                        left outer join (select sum(coalesce(product_template.list_price,0)) as price_nega, sale_order_line.order_partner_id from sale_order_line
                        inner join product_template on sale_order_line.product_id = product_template.id group by sale_order_line.order_partner_id) as tabla2
                        on  tabla1.partner_id  = tabla2.order_partner_id where tabla1.partner_id =%d """ % i)
            sql_res = cr.dictfetchone()
            if sql_res:
                res[i.id] = sql_res['x']
                partner = self.pool.get('res.partner').browse(cr,uid,ids, context=None)
                partner.write({'puntos': sql_res['x']})
            else:
            #res[i] debe ponerse a False y no a None a causa de XML:RPC
            # "cannot marshal None unless allow_none is enabled"
                res[i.id] = False
        return res


    _columns = {

        'puntos':fields.integer(),
        'loyalty_points': fields.function(get_restant_points,digits = (6,0)),
        'loyalty_supplier_id': fields.many2one('loyalty.supplier','partner_id'),
        'product_id': fields.many2one('product.template', 'Producto')
        
    }


class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {

        'list_price': fields.integer('Puntos Extra de Fidelidad',digits = (6,0)),
    }

    _sql_constraints = {('default_code', 'unique(default_code)','El Numero del Producto debe ser unico!')}


class website(osv.osv):
    _inherit = 'website'

    def _get_points(self, cr, uid, ids, context=None):
        partner = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id
        cr.execute("""select coalesce(p - coalesce(price_nega,0),0)  as x
                        from (select sum(coalesce(puntos,0)) as p, partner_id from loyalty_supplier group by partner_id ) as  tabla1
                        left outer join (select sum(coalesce(product_template.list_price,0)) as price_nega, sale_order_line.order_partner_id from sale_order_line
                        inner join product_template on sale_order_line.product_id = product_template.id group by sale_order_line.order_partner_id) as tabla2
                        on  tabla1.partner_id  = tabla2.order_partner_id where tabla1.partner_id =%d """ %partner)
        sql_res = cr.dictfetchone()
        if sql_res:
            res = sql_res['x']

        else:
            #res[i] debe ponerse a False y no a None a causa de XML:RPC
            # "cannot marshal None unless allow_none is enabled"
                res = False
        return res

