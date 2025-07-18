# -*- coding: utf-8 -*-
#
#   OghmaNano - Organic and hybrid Material Nano Simulation tool
#   Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.oghma-nano.com
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#   SOFTWARE.
#

## @package tab_terminal
#  The terminal tab, used to display simulation progress.
#


from PySide2.QtWidgets import QTabWidget,QTextEdit,QWidget,QHBoxLayout
from gQtCore import QProcess, Qt
from PySide2.QtGui import QPalette,QColor,QFont

from QHTabBar import QHTabBar

import multiprocessing
import functools
from cpu_usage import cpu_usage
from win_lin import get_platform
from hpc import hpc_class
from global_objects import global_object_register
from jobs import jobs_view
from server import server_get

from css import css_apply
from cal_path import multiplatform_exe_command
import shlex
import subprocess
import time
from gQtCore import gSignal
from threading import Thread
from json_c import json_local_root

class QProcess2(QWidget):
	readyRead = gSignal()
	def __init__(self):
		QWidget.__init__(self)
		self.running=False
		self.path=None
		self.data=bytearray()
		self.read_pos=0

	def rod(self,command):
		rc=None
		self.data=bytes()
		self.read_pos=0
		#print(shlex.split(command))
		process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=self.path)
		while True:
			output = process.stdout.readline()
			#print(len(output),rc,output)
			if len(output) == 0:
				if rc is not None:
					print("break 1")
					break
			if output:
				#print(type(output),type(self.data))
				self.data=self.data + output
				self.readyRead.emit()
				#print(">>",output.strip())

			#print(command)
			rc = process.poll()
			time.sleep(0.001)

		
		print("1thread quit",len(self.data),self.read_pos)
		while True:
			print(len(self.data),self.read_pos)
			if len(self.data)==self.read_pos:
				break
			time.sleep(0.01)

		print("2thread quit",len(self.data),self.read_pos)
		self.running=False
		print(self.data)

	def start(self,command):
		th = Thread(target=self.rod, args=(command,))
		th.daemon = False
		th.start()

	def state(self):
		if self.running==True:
			return QProcess.Running
		else:
			return QProcess.NotRunning

	def setWorkingDirectory(self,path):
		self.path=path
		
	def readAll(self):
		stop=len(self.data)
		start=self.read_pos
		ret=self.data[start:stop]
		self.read_pos=self.read_pos+(stop-start) 
		return ret

class output_box(QTextEdit):
	def __init__(self,device_type):
		QTextEdit.__init__(self)
		self.font = QFont()
		self.font.setFamily('Monospace')
		self.font.setStyleHint(QFont.Monospace)
		self.font.setFixedPitch(True)
		self.font.setPointSize(int(12))
		
		self.setFont(self.font)
		pal = QPalette()
		bgc = QColor(0, 0, 0)
		pal.setColor(QPalette.Base, bgc)
		textc = QColor(230, 230, 230)
		pal.setColor(QPalette.Text, textc)
		self.setPalette(pal)
		self.device_type=device_type
		self.setAcceptRichText(False)
		#self.setContextMenuPolicy(Qt.NoContextMenu)
		#self.setOpenLinks(False)
		self.setReadOnly(True)
		self.setUndoRedoEnabled(False)

	def add_text(self,data):
		self.setUpdatesEnabled(False);
		cursor = self.textCursor()
		cursor.movePosition(cursor.End,cursor.MoveAnchor)
		self.setTextCursor(cursor)
		cursor.insertHtml(data)
		self.ensureCursorVisible()
		self.setUpdatesEnabled(True)

class tab_terminal(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.tab=QTabWidget()
		css_apply(self.tab,"style_h.css")
		self.vbox=QHBoxLayout()
		self.vbox.addWidget(self.tab)
		self.usage=cpu_usage()
		self.vbox.addWidget(self.usage)
		self.setLayout(self.vbox)
		self.my_server=server_get()

	def dataReady(self,i):
		#cursor = self.terminals[i].textCursor()
		#cursor.movePosition(cursor.End,cursor.MoveAnchor)
		#self.terminals[i].setTextCursor(cursor)
		r=self.process[i].readAll()
		data=str(r,'utf-8',errors='ignore')

		#cursor.insertHtml(data)
		pos=data.find('<clear_terminal>')
		if pos!=-1:
			data=data[pos:]
			self.terminals[i].clear()
		#print("\n'"+data+"'\n")
		self.terminals[i].add_text(data)


	def list_cpu_state(self):
		for i in range(0,self.cpus):
			if self.process[i].state()==QProcess.NotRunning:
				print(i,"0")
			else:
				print(i,"1")

	def clear(self):
		self.terminals[0].clear()

	def run(self,path,command):
		for i in range(0,self.cpus):
	
			if self.process[i].state()==QProcess.NotRunning:
				cursor = self.terminals[i].textCursor()
				self.terminals[i].clear()
				cursor.insertHtml(_("Running: ")+command+"<br>")
				cursor.insertHtml(path+"<br>")
				self.process[i].setWorkingDirectory(path)

				command=multiplatform_exe_command(command,port=self.my_server.server.ipc.port)
				print(command)
				#os.system(command)
				#print("path: "+path)
				#print("call: "+command)
				self.process[i].start(command)
				return True

		print(_("I could not find a free cpu to run the command on"))
		return False

	def test_free_cpus(self):
		ret=0
		for i in range(0,self.cpus):
	
			if self.process[i].state()==QProcess.NotRunning:
				ret=ret+1

		return ret
	
	def init(self):
		self.cpus=multiprocessing.cpu_count()
		
		self.tab.setTabsClosable(True)
		self.tab.setMovable(True)
		self.tab.setTabBar(QHTabBar())
		self.tab.setTabPosition(QTabWidget.West)


		self.terminals=[]
		self.process=[]
		for i in range(0,self.cpus):
			term=output_box("local_cpu")

			#proc=QProcess2()
			proc=QProcess(self)

			proc.readyRead.connect(functools.partial(self.dataReady,i))
			self.process.append(proc)
			self.terminals.append(term)
			self.tab.addTab(term,_("CPU")+" "+str(i))


		self.cluster_output=output_box("cluster_node")
		self.tab.addTab(self.cluster_output,_("Cluster"))
					
		self.jview=jobs_view()
		#self.jview.load_data(self.myserver.cluster_jobs)
		self.tab.addTab(self.jview,"Jobs list")

		if json_local_root().get_token_value("gui_config","enable_betafeatures")==True:
			self.cluster=hpc_class()
			self.tab.addTab(self.cluster,_("Nodes"))
			global_object_register("cluster_tab",self.cluster)

		global_object_register("clear_terminal",self.clear)

		self.my_server.new_message.connect(self.data_from_cluster)

	def data_from_cluster(self,data):
		#self.cluster_output.add_text(data+"\n")
		print(data+"\n")

	def help(self):
		my_help_class.help_set_help("utilities-terminal.png","<big><b>The terminal window</b></big>\nThe model will run in this window.  You can also use it to enter bash commands.")

