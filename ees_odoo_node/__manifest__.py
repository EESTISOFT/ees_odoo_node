{
    'name': 'EESTISOFT odoo node-js',
    'version': '11.0.4.8',
	'license':'LGPL-3', 
    'author': 'EESTISOFT, ' 'Hideki Yamamoto, ' 'Tiago Magrini Rigo',
	'mantainer':'EESTISOFT',
    'category': 'Productivity',
	'support':'odoo@eestisoft.com',
    'website': 'https://eestisoft.com',
    'sequence': 2,
    'summary': 'Adds nodejs',
    'description': """
EESTISOFT module that Adds nodejs to odoo
	
Made with love.
    """,
    'images':['Banner.png'],
    'depends': ['base'],
    'data': ['views/ees_odoo_node.xml','views/ir.model.access.csv'],
    'installable': True,
    'application': True,
    'auto_install': False
}
