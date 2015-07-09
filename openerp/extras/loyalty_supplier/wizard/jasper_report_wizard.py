# -*- coding: utf-8 -*-
##############################################################################

from openerp.osv import fields, osv
class loyalty_report_supplier_wizard(osv.osv_memory):
    _name="loyalty.report.supplier_wizard"
    _columns={
              'partner_id':fields.many2one('res.partner',"Cliente",required=True)
              }

    def check_report(self, cr, uid, ids, context=None):
        data={}
        data['model']='res.partner'
        data['ids']=ids
        data['origin_records']=False
        data.update({'parameters':{
                            'partner_id':self.browse(cr,uid,ids[0]).partner_id.id
                            }
                  })
        r= {
                'type':'ir.actions.report.xml',
                'report_name':'report_loyalty',
                'datas':data,
        }
        return r
loyalty_report_supplier_wizard()
