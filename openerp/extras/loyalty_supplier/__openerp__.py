# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE Johan Olano (<http:http://www.ias.com.co).
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
{
    "name": "Fidelizacion de Clientes",
    #"version": "1.0",
    #"description": """
    #En este modulo se imprementa la sumatoria de puntos segun los Datos Cargados Por la Compañia
     
    #Colaboradores:
    #- Johan Alejandro Olano <jolano@ias.com.co>
    #- Julián Andrés García Álvarez <jgarcia@ias.com.co>
    
    #""",
    "author": "I.A.S. Ingenieria, Aplicaciones y Software",
    #"website": "http://www.ias.com.co",
    "category": "Fidelizacion",
    "depends": ["base", "product", 'website_sale','jasper_reports'],
    "data": ['views/loyalty_supplier_view.xml','views/templates.xml','report/report.xml','wizard/report_wizard_view.xml'],
    "active": False,
    "installable": True,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
