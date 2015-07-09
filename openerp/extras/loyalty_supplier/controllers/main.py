from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.extras.website_sale.controllers.main import (
website_sale
)

class WebsiteSale(website_sale):

    @http.route()
    def checkout(self, **post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_user = registry.get('res.users')
        partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        cr.execute("""select coalesce(p - coalesce(price_nega,0),0)  as x
                            from (select sum(coalesce(puntos,0)) as p, partner_id from loyalty_supplier group by partner_id ) as  tabla1
                            left outer join (select sum(coalesce(product_template.list_price,0)) as price_nega, sale_order_line.order_partner_id from sale_order_line
                            inner join product_template on sale_order_line.product_id = product_template.id group by sale_order_line.order_partner_id) as tabla2
                            on  tabla1.partner_id  = tabla2.order_partner_id where tabla1.partner_id =%d """ % partner_id)
        sql_res = cr.dictfetchone()
        if sql_res:
            if sql_res['x'] <  request.website.sale_get_order().amount_total:


                return request.website._render("loyalty_supplier.modal_warning")

            else:
                    order = request.website.sale_get_order(force_create=1, context=context)

                    redirection = self.checkout_redirection(order)
                    if redirection:
                        return redirection

                    values = self.checkout_values()

                    return request.website.render("website_sale.checkout", values)
