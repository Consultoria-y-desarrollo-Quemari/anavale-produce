{
    'name': 'Anavale Produce',
    'category': 'Uncategorized',
    'version': '0.1',
    'summary': 'Anavale Produce',
    'description': """ This module allows Purchase Order to select Lot from available Lots, 
    including in-transit lots.
    Warehouse has to be configured as a 'Receive goods in input and then stock (2 steps)'.
    """,
    "author" : "Mayte Montano",
    'sequence': 1,
    "email": 'mayte@eadminpro.com',
    "website":'http://eadminpro.com/',
    'depends': ['sale_stock', 'percent_field', 'sale', 'stock','purchase'],
    'data': [
            'security/ir.model.access.csv',
            'views/sale_view.xml',
            'views/stock_view.xml',
            'views/stock_quant_view.xml',
            'views/stock_quality_view.xml',
            'views/product_view.xml',
            'views/res_partner_views.xml',
            'views/sale_portal_sidebar_template.xml',
            'views/lot_view.xml',
            'views/purchase_view.xml',
            'wizard/partner_sequence_change_view.xml',
            'wizard/quant_lot_repack_view.xml',
            'wizard/sale_report_avg_wz_view.xml',
            'wizard/quant_product_repack_view.xml',
            'data/report_paperformat.xml',
            'data/purchase_order_action_server.xml',
            'report/sale_report.xml',
            'report/sale_report_templates.xml',
            'report/quality_report_views.xml',
            'report/report_quality.xml',
            'report/sale_report_avg_views.xml',
            'report/sale_report_by_lot_views.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
#na