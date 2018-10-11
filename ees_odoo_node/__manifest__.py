{
    'name': 'EESTISOFT odoo node-js',
    'version': '11.0.4.8',
    'author': 'Hideki Yamamoto',
    'category': 'Productivity',
    'website': 'https://eestisoft.com',
    'sequence': 2,
    'summary': 'Adds nodejs',
    'description': """
Adds nodejs
	
Made with love.
    """,
    'depends': ['base'],
    'data': ['views/ees_odoo_node.xml','views/ir.model.access.csv'],
    'installable': True,
    'application': True,
    'auto_install': False
}
