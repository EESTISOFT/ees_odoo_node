# -*- coding: utf-8 -*-
# © 2017 Hideki Yamamoto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
	

import os
import signal
from odoo import api, fields, models
from datetime import datetime
import servicemanager
import win32api
import win32process
import win32service
import win32serviceutil

import subprocess
import sys
from os.path import dirname, join, split


class ees_odoo_node_configt(models.Model):
	_name='ees_odoo_node.config'
	name=fields.Char('Name')
	nodejs_folder=fields.Char('Node-Js Folder')
	pgconfig=fields.Text('Postgres config')
	dbtools=fields.Text('DB tools')
	postexe=fields.Text('Post exe')
	@api.depends('nodejs_folder')
	def install_node_modules(self):
		for record in self:
			fld=record.nodejs_folder			
			subprocess.Popen([fld+'npm.cmd', 'i','pg','pg-escape','--save','--prefix',fld])
	
class ees_odoo_node_script(models.Model):
	_name='ees_odoo_node.script'
	name=fields.Char('Name')
	desc=fields.Text('Description')
	active = fields.Boolean('Active', default=True)
	jscontents=fields.Text('script content', default='\n\n\n\n\n\n\n\n')	
	console_js=fields.Text('console output')
	cfg=fields.Many2one('ees_odoo_node.config',default=1)
	pid=fields.Integer('pid')

	@api.multi
	@api.depends('jscontents')
	def run_script_once(self):
		for record in self:
			if record.jscontents:
				fname='script'+str(record.id)+'.js'
				fld=record.cfg.nodejs_folder
				ttt='const scriptfile="'+fld.replace('\\','\\\\')+fname+'";const script_dbid='+str(record.id)+';const br="<br/>";'
				sss=record.cfg.dbtools.replace('%PG-CONFIG',record.cfg.pgconfig)
				with open(fld+fname, 'w+') as out:
					out.write(ttt+sss+record.jscontents+'\n')
				with open(fld+'c-'+fname, 'w+') as oout:
					oout.write(ttt+record.cfg.postexe.replace('%PG-CONFIG',record.cfg.pgconfig)+'\n')
				#windows
				p=subprocess.Popen([fld+'node.exe',fld+'c-'+fname])
				record.pid=p.pid

	def stop_script_once(self):
		for record in self:
			if record.pid:
				ppid=record.pid
				record.pid=0
				record.console_js='ODOO CLIENT'+' - Forcefully stopped\n'+record.console_js
				if ppid>0:
					try:
						#windows
						subprocess.call(['taskkill', '/F', '/T', '/PID', str(ppid)])
					except ValueError:
						record.pid=0
				
	def fake_refresh(self):
		for record in self:
			sss=''

	def clean_console(self):
		for record in self:
			record.console_js=''

	@api.depends('jscontents','cfg')
	def add_db_caps(self):
		for record in self:
			sss=record.cfg.dbtools.replace('%PG-CONFIG',record.cfg.pgconfig)
			if record.jscontents:
				record.jscontents=sss+'\n\n'+record.jscontents.replace(sss,'')
			else:
				record.jscontents=sss+'\n\n'
	