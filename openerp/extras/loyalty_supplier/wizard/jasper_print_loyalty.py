# -*- coding: utf-8 -*-
##############################################################################

from openerp.extras.jasper_reports import jasper_report
from openerp import pooler
from openerp.extras.loyalty_supplier.report import jasper_data_parser

class jasper_print_loyalty(jasper_data_parser.JasperDataParser):

    def __init__(self, cr, uid, ids, data, context):

        if context is None:
            context = {}
        super(jasper_print_loyalty,self).__init__(cr, uid, ids, data, context)

    def generate_records(self, cr, uid, ids, data, context):
        records = self.browse(cr, uid, ids)
        return records

    def generate_data_source(self, cr, uid, ids, data, context):
        if not(data['origin_records']):
            return False
        else:
            return 'records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return data.get('parameters',False)

jasper_report.report_jasper(
                            'report.report_loyalty',
                            'res.partner',
                            parser=jasper_print_loyalty
                            )
