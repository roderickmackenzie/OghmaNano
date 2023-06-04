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

## @package ribbon_sim_mode
#  The sim mode ribbon.
#


from cal_path import get_css_path

#qt
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from win_lin import desktop_open

#windows
from help import help_window
from error_dlg import error_dlg
from server import server_get

from global_objects import global_object_run
from icon_lib import icon_get

from cal_path import sim_paths
from play import play
from util import wrap_text

from gQtCore import gSignal

from global_objects import global_object_register

from lock import get_lock

from help import help_window
from QAction_lock import QAction_lock
from lock import get_lock
from json_root import json_root
from ribbon_page import ribbon_page

class gQAction(QAction_lock):
	selected=gSignal(QAction_lock)

	def __init__(self,s,obj,command,module,actions):
		if module=="ray":
			module="trace"
		elif module=="transfer_matrix":
			module="optics"

		self.command=command
		self.module=module
		self.icon_name=obj.icon
		self.id=obj.id
		self.over=False
		self.name=obj.name
		self.text=obj.name.replace("\\n","\n")
		self.actions=actions
		
		QAction_lock.__init__(self,self.icon_name, self.text, s,self.module)
		self.setCheckable(True)
		self.clicked.connect(self.callback_click)
		self.hovered.connect(self.callback_hover)

	def callback_click(self):
		data=json_root()
		data.sim.simmode=self.command+"@"+self.module
		data.save()
		self.selected.emit(self)

	def get_simmode(self):
		a=self.command+"@"+self.module
		return a.lower()

	def callback_hover(self):
		for a in self.actions:
			a.over=False
			if self==a:
				a.over=True

class ribbon_sim_mode(ribbon_page):

	def callback_click(self,w,disable_help=False):
		self.blockSignals(True)
		for a in self.actions:
			if type(a)==gQAction:
				a.setChecked(False)

		w.setChecked(True)
		if disable_help==False:
			if w.icon!=False and w.text!=None:
				help_window().help_set_help([w.icon_name+".png",_("<big><b>Simulation mode changed</b></big><br>"+w.name.replace("\\n"," "))])

		self.blockSignals(False)

	def update(self):
		data=json_root()
		self.clear_toolbar()

		self.blockSignals(True)

		found=False
		simmode=data.sim.simmode.lower()

		for segment_name in data.sims.var_list:
			segment_name=segment_name[0]
			segs=getattr(data.sims,segment_name,None)
			if segs!=None:
				segs=getattr(segs,"segments",None)

			if segs!=None:
				i=0
				added=0
				for sub_sim in segs:
					added=added+1
					a = gQAction(self, sub_sim,"segment"+str(i), segment_name,self.actions)
					a.selected.connect(self.callback_click)
					
					self.actions.append(a)
					self.addAction(a)
					if a.get_simmode()==simmode:
						self.callback_click(a,disable_help=True)
						
						found=True

					i=i+1
				if added!=0:
					self.addSeparator()


		#if there is no known mode, just set it to jv mode
		if found==False:
			for a in self.actions:
				if type(a)==gQAction:
					if a.module=="jv":
						self.callback_click(a,disable_help=True)
						data=json_root()
						data.sim.simmode=a.command+"@"+a.module
						data.save()
						break

			self.blockSignals(False)

	def clear_toolbar(self):
		self.clear()
		self.actions=[]

	def __init__(self):
		ribbon_page.__init__(self)
		self.actions=[]
		self.dont_show=["photon_extraction"]
		self.myserver=server_get()

		self.main_menu = QMenu(self)
		action=self.main_menu.addAction(icon_get("list-remove"),_("Delete"))
		action.triggered.connect(self.callback_delete)
		
		global_object_register("ribbon_sim_mode_update",self.update)

	def setEnabled(self,val):
		self.undo.setEnabled(val)
		self.run.setEnabled(val)
		#self.stop.setEnabled(val)
		self.scan.setEnabled(val)
		self.plot.setEnabled(val)
		self.sun.setEnabled(val)
		self.help.setEnabled(val)



	def mouseReleaseEvent(self,event):
		if event.button()==Qt.RightButton:
			self.main_menu.exec_(event.globalPos())

	def callback_delete(self):
		i=0
		for a in self.actions:
			if a.over==True:
				self.removeAction(a)
				self.actions.pop(i)
				obj=json_root().sims.find_object_by_id(a.id)
				for segment_name in json_root().sims.var_list:
					segment_name=segment_name[0]
					segs=getattr(json_root().sims,segment_name,None)
					if segs!=None:
						segs=getattr(segs,"segments",None)
						ii=0
						for o in segs:
							if o==obj:
								segs.pop(ii)
					json_root().save()
				break
			i=i+1
