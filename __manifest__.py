{
    'name': "CFR",
    'description': """
       This module add/changes functionalities.
    """,
    'author': "Hemangi Rupareliya <rupareliyahemangi145@gmail.com>",
    'version': "15.0.1.0.0",
    'depends': ['contacts', 'sale_management', 'sale_crm', 'account', 'sms', 'maintenance','sale_pricelist'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/crm_views.xml',
        'views/sale_order_views.xml',
        'views/territory_detail.xml',
        'views/ship_terms.xml',
        'views/terms_detail.xml',
        'views/ship_via_detail.xml',
        'views/pricelist_tree.xml',
        'views/product_category.xml',
        'views/pre_data.xml',
    ],
     'demo': [],
    'installable': True,
    'application':True,
    'sequence': -100,
    'auto_install': False,
    'assets': {},
    'license': "LGPL-3"
}
