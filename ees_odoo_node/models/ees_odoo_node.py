# -*- coding: utf-8 -*-
# © 2018 Hideki Yamamoto
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
from subprocess import Popen, PIPE
import sys
from os.path import dirname, join, split
from time import sleep



class ees_odoo_node_configt(models.Model):
	_name='ees_odoo_node.config'
	name=fields.Char('Name')
	nodejs_folder=fields.Char('Node-Js Folder')
	nssm_folder=fields.Char('NSSM Folder')
	pgconfig=fields.Text('Postgres config')
	dbtools=fields.Text('DB tools')
	postexe=fields.Text('Post exe')
	service=fields.Text('Service')
	createFile=fields.Text('Create File')
	dbAccess=fields.Text('DB Access')
	testNode = fields.Boolean('Test Node', default=False)
	testNpm = fields.Boolean('Test Npm', default=False)
	testDbAccess = fields.Boolean('Test DB Access', default=False)
	testDbWrite = fields.Boolean('Test DB Write', default=False)
	
	@api.depends('nodejs_folder')
	def install_node_modules(self):
		for record in self:
			fld=record.nodejs_folder			
			subprocess.Popen([fld+'npm.cmd', 'i','pg','pg-escape','--save','--prefix',fld])
			

	#  sets the boolean result test field to false!
	@api.depends('testNode','testNpm','testDbAccess','testDbWrite')
	def set_all_test_false(self):
		for record in self:
			record.testNode = False
			record.testNpm = False
			record.testDbAccess = False
			record.testDbWrite = False

	def read_file(self):
		file = open('eesti.txt', 'r')
		self.testNode = True

	@api.depends('testNode','createFile')
	def test_node_file(self):
		for record in self:
			fname='scriptCreateFile'+str(record.id)+'.js'
			fld=self.nodejs_folder
			ttt='const scriptfile="'+fld.replace('\\','\\\\')+fname+'";const script_dbid='+str(record.id)+';const br="<br/>";'
			sss=self.dbtools.replace('%PG-CONFIG',self.pgconfig)
			with open(fld+fname, 'w+') as out:
				out.write(ttt+sss+self.createFile+'\n')
			with open(fld+'c-'+fname, 'w+') as oout:
				sss=self.createFile.replace('%PG-CONFIG',self.pgconfig)+'\n'
				sss=sss.replace('%NODEFOLDER',fld.replace('\\','\\\\'))
				oout.write(ttt+sss)
			#windows
			p=subprocess.Popen([fld+'node.exe',fld+'c-'+fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			(stdout, stderr) = p.communicate()
			exit_code = p.wait()
			if exit_code != 0:
					#testNode = False
					self.testNode = False
					return stderr
			else:
					#read_file
					file = open('eesti.txt', 'r')
					self.testNode = True
					
	@api.depends('testNpm')
	def test_npm(self):
		fld=self.nodejs_folder
		if (((os.path.isdir(fld+'/node_modules/pg'))) and ((os.path.exists(fld+'/node_modules/pg')))):
			self.testNpm = True
		else:
			self.testNode = False
	
	@api.depends('testDbAccess','dbAccess')
	def test_db_access(self):
		for record in self:
			fname='scriptDbAccess'+str(record.id)+'.js'
			fld=self.nodejs_folder
			ttt='const scriptfile="'+fld.replace('\\','\\\\')+fname+'";const script_dbid='+str(record.id)+';const br="<br/>";'
			sss=self.dbtools.replace('%PG-CONFIG',self.pgconfig)
			with open(fld+fname, 'w+') as out:
				out.write(ttt+sss+self.dbAccess+'\n')
			with open(fld+'c-'+fname, 'w+') as oout:
				sss=self.dbAccess.replace('%PG-CONFIG',self.pgconfig)+'\n'
				sss=sss.replace('%NODEFOLDER',fld.replace('\\','\\\\'))
				oout.write(ttt+sss)
			#windows
			p=subprocess.Popen([fld+'node.exe',fld+'c-'+fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			(stdout, stderr) = p.communicate()
			exit_code = p.wait()
			if exit_code != 0:
					self.testDbAccess = False
					return stderr
			else:
					self.testDbAccess = True
					return stdout
	
	@api.depends('testDbWrite')
	def test_db_write(self):
		try:
			self.env.cr.execute('insert into ees_odoo_node_config values (666)')
			self.env.cr.execute('delete from ees_odoo_node_config values where id=(666)')
			self.testDbWrite = True
			return True
		except Exception:
			self.testDbWrite = False
		else:
			self.testDbWrite = False

class ees_odoo_node_script(models.Model):
	_name='ees_odoo_node.script'
	name=fields.Char('Name')
	desc=fields.Text('Description')
	active = fields.Boolean('Active', default=True)
	jscontents=fields.Text('script content', default='\n\n\n\n\n\n\n\n')	
	console_js=fields.Text('console output')
	console_service=fields.Text('service console output')
	cfg=fields.Many2one('ees_odoo_node.config',default=1)
	pid=fields.Integer('pid')
	dayTime=fields.Char('Day Time')
	frequency=fields.Selection((('HOURLY', 'HOURLY'),('DAILY', 'DAILY'),('WEEKLY', 'WEEKLY'),('MONTHLY', 'MONTHLY')), string='Frequency')
	
	
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
					sss=record.cfg.postexe.replace('%PG-CONFIG',record.cfg.pgconfig)+'\n'
					sss=sss.replace('%NODEFOLDER',fld.replace('\\','\\\\'))
					oout.write(ttt+sss)
				#windows
				p=subprocess.Popen([fld+'node.exe',fld+'c-'+fname])
				record.pid=p.pid

	def stop_script_once(self):
		for record in self:
			if record.pid:
				ppid=record.pid
				record.pid=0
				if not record.console_js:
					record.console_js=''
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
	
	def clean_console_service(self):
		for record in self:
			record.console_service=''
			
	@api.multi
	@api.depends('jscontents','cfg')
	def install_service(self):
		for record in self:
			if record.jscontents:
				fname='script'+str(record.id)+'.js'
				fld=record.cfg.nodejs_folder
				ttt='const scriptfile="'+fld.replace('\\','\\\\')+fname+'";const script_dbid='+str(record.id)+';const br="<br/>";'
				sss=record.cfg.dbtools.replace('%PG-CONFIG',record.cfg.pgconfig)
				with open(fld+fname, 'w+') as out:
					out.write(ttt+sss+record.jscontents+'\n')
				with open(fld+'svc-'+fname, 'w+') as oout:
					sss=record.cfg.service.replace('%PG-CONFIG',record.cfg.pgconfig)+'\n'
					sss=sss.replace('%NODEFOLDER',fld.replace('\\','\\\\'))
					oout.write(ttt+sss)
				#windows
				fldNSSM=record.cfg.nssm_folder
				p=subprocess.Popen([fldNSSM+'nssm.exe', 'install', fname, fld+'node.exe', 'svc-'+fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
				record.pid=p.pid          
				
	def remove_service(self):
		fname='script'+str(self.id)+'.js'
		fld=self.cfg.nssm_folder
		proc = subprocess.Popen([fld+'nssm', 'remove', fname, 'confirm'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	def state_service(self):
		fname='script'+str(self.id)+'.js'
		fld=self.cfg.nssm_folder
		proc = subprocess.Popen([fld+'nssm', 'status', fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	def start_service(self):
		fname='script'+str(self.id)+'.js'
		fld=self.cfg.nssm_folder
		proc = subprocess.Popen([fld+'nssm', 'start', fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	def stop_service(self):
		fname='script'+str(self.id)+'.js'
		fld=self.cfg.nssm_folder
		proc = subprocess.Popen([fld+'nssm', 'stop', fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	
	def schedule_task(self):
		fname='script'+str(self.id)+'.js'
		fld=self.cfg.nodejs_folder
		#	SchTasks /Create /SC DAILY /TN “My Task” /TR “C:RunMe.bat” /ST 09:00
		proc = subprocess.Popen(['SchTasks', 'Create', '/SC', 'DAILY', '/TN', '\"'+fname+'\"', '/TR', '\"'+fld+fname+'\"', '/ST', '09:00'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

	
	@api.depends('jscontents','cfg')
	def add_db_caps(self):
		for record in self:
			sss=record.cfg.dbtools.replace('%PG-CONFIG',record.cfg.pgconfig)
			if record.jscontents:
				record.jscontents=sss+'\n\n'+record.jscontents.replace(sss,'')
			else:
				record.jscontents=sss+'\n\n'
	