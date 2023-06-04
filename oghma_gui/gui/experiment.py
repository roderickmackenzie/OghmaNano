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

## @package experiment
#  The main experiment window, used for configuring time domain experiments.
#

from dlg_get_text2 import dlg_get_text2
from global_objects import global_object_get
from icon_lib import icon_get
from global_objects import global_object_register
import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar, QListWidget, QListWidgetItem, QMenu, QListView
from PySide2.QtGui import QPainter,QIcon

#window
from time_domain_experiment_tab import time_domain_experiment_tab
from detectors_tab import detectors_tab
from tab_light_src import tab_light_src
from tab_probes import tab_probes
from cluster_tab import cluster_tab

from QHTabBar import QHTabBar
from gui_util import yes_no_dlg
from gQtCore import gSignal
from util import wrap_text
from QWidgetSavePos import QWidgetSavePos
from css import css_apply

from progress_class import progress_class
from process_events import process_events

from ribbon_experiment import ribbon_experiment
from json_root import json_root
import copy
from global_objects import global_object_run
from cal_path import sim_paths
from json_local_root import json_local_root

class experiment(QWidgetSavePos):

	changed = gSignal()
	delete_item = gSignal(str)
	rename_item = gSignal(str,str)

	def update(self):
		for i in range(0,self.notebook.count()):
			w=self.notebook.widget(i)
			w.update()


	def load_tabs(self):

		progress_window=progress_class()
		progress_window.show()
		progress_window.start()

		process_events()
		i=0
		if self.style=="tabs":
			exec("from "+self.name_of_tab_class+" import "+self.name_of_tab_class)

			data=self.get_json_obj()
			for sim in data.segments:
				tab=eval(self.name_of_tab_class+"(sim)")
				#tab=time_domain_experiment_tab(sim)
				tab.uid=sim.id
				self.notebook.addTab(tab,sim.name)

				progress_window.set_fraction(float(i)/float(len(data.segments)))
				progress_window.set_text(_("Loading")+" "+sim.name)
				process_events()
				i=i+1
		else:
			self.notebook.clear()
			data=self.get_json_obj()
			for sim in data.segments:
				itm = QListWidgetItem( sim.name )
				a=icon_get(sim.icon)
				itm.setIcon(a)
				self.notebook.addItem(itm)

		progress_window.stop()
		self.update_interface()

	def clear_pages(self):
		self.notebook.clear()

	def __init__(self,name_of_tab_class,window_save_name="time_domain_experiment", window_title=_("Time domain experiment window"),json_search_path=None,icon="icon",style="tabs",min_y=700):
		QWidgetSavePos.__init__(self,window_save_name)
		self.main_vbox = QVBoxLayout()
		self.json_search_path=json_search_path
		self.name_of_tab_class=name_of_tab_class
		self.setMinimumSize(800, min_y)
		self.setWindowTitle2(window_title)
		self.setWindowIcon(icon_get(icon))
		self.style=style

		self.ribbon=ribbon_experiment()
		#self.ribbon.tb_save.triggered.connect(self.callback_save)

		#self.ribbon.tb_laser_start_time.triggered.connect(self.callback_laser_start_time)

		#self.ribbon.tb_start.triggered.connect(self.callback_start_time)


		self.main_vbox.addWidget(self.ribbon)

		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


		if self.style=="tabs":
			self.notebook = QTabWidget()
			css_apply(self.notebook ,"style_h.css")
			self.tab_bar=QHTabBar()
			self.notebook.setTabBar(self.tab_bar)
			self.notebook.setTabPosition(QTabWidget.West)
			self.notebook.setMovable(True)

			self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			
			self.tab_bar.rename.connect(self.callback_rename_page)
			self.tab_bar.delete.connect(self.callback_delete_page)
			self.tab_bar.paste.connect(self.do_paste)
			self.tab_bar.tabMoved.connect(self.callback_tab_moved)
		elif self.style=="list":
			self.notebook = QListWidget()
			self.notebook.setIconSize(QSize(64,64))
			self.notebook.setViewMode(QListView.IconMode)
			self.notebook.itemDoubleClicked.connect(self.on_item_activated)
			self.notebook.setContextMenuPolicy(Qt.CustomContextMenu)
			self.notebook.customContextMenuRequested.connect(self.callback_menu)

		self.main_vbox.addWidget(self.notebook)
		self.status_bar=QStatusBar()
		self.main_vbox.addWidget(self.status_bar)

		self.setLayout(self.main_vbox)

		self.load_tabs()

		self.ribbon.tb_clone.triggered.connect(self.callback_clone_page)
		self.ribbon.tb_rename.triggered.connect(self.callback_rename_page)
		self.ribbon.tb_delete.triggered.connect(self.callback_delete_page)

		self.ribbon.tb_new.triggered.connect(self.callback_add_page)

		if self.style=="tabs":
			self.notebook.currentChanged.connect(self.update_interface)
		elif self.style=="list":
			self.notebook.itemSelectionChanged.connect(self.update_interface)


		self.fixup_new=None

	def callback_rename_page(self):
		found,tab = self.get_current_item()
		if found==True:
			data=json_root()
			new_sim_name=dlg_get_text2( _("Rename:"), tab.name,"rename.png")

			new_sim_name=new_sim_name.ret
			
			if new_sim_name!=None:
				obj=data.find_object_by_id(tab.uid)
				old_sim_name=obj.name
				obj.name=new_sim_name
				if self.style=="tabs":
					self.notebook.setTabText(self.notebook.currentIndex(), new_sim_name)
				else:
					self.load_tabs()
				data.save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()
				self.rename_item.emit(old_sim_name,new_sim_name)

	def callback_clone_page(self):
		found, tab = self.get_current_item()
		if found==True:
			data=self.get_json_obj()
			obj=data.find_object_by_id(tab.uid)
			new_sim_name=dlg_get_text2( _("Clone:"), obj.name+"_new","clone.png")

			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				a=copy.deepcopy(obj)
				a.name=new_sim_name
				a.update_random_ids()
				data=self.get_json_obj()
				data.segments.append(a)
				if self.style=="tabs":
					tab=eval(self.name_of_tab_class+"(data.segments[-1])")
					self.notebook.addTab(tab,new_sim_name)
				else:
					self.load_tabs()
				json_root().save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()

	def callback_delete_page(self):
		data=self.get_json_obj()
		found, tab = self.get_current_item()
		if found==True:
			obj=data.find_object_by_id(tab.uid)
			response=yes_no_dlg(self,_("Are you sure you want to delete : ")+obj.name.replace("\n"," "))
			if response == True:
				index=self.notebook.currentIndex()
				data.segments.remove(obj)
				if self.style=="tabs":
					self.notebook.removeTab(index)
				else:
					self.load_tabs()
				json_root().save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()

				self.delete_item.emit(obj.name)

	def callback_add_page(self):
		found,tab = self.get_current_item()
		if found==True:
			obj=self.get_json_obj().find_object_by_id(tab.uid)
			new_name=obj.name+"_new"
		else:
			new_name="new"

		new_sim_name=dlg_get_text2( _("Make a new:"), new_name,"document-new.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:

			exec("from "+self.name_of_tab_class+" import "+self.name_of_tab_class)

			data=self.get_json_obj()
			if data.segment_examples[0]==None:
				dfasdasd

			a=copy.deepcopy(data.segment_examples[0])
			a.name=new_sim_name
			a.update_random_ids()
			if self.fixup_new!=None:
				self.fixup_new(a)
			data.segments.append(a)
			if self.style=="tabs":
				tab=eval(self.name_of_tab_class+"(data.segments[-1])")
				tab.uid=a.id
				self.notebook.addTab(tab,new_sim_name)
			else:
				self.load_tabs()

			json_root().save()
			global_object_run("ribbon_sim_mode_update")
			self.changed.emit()

	def get_current_item(self):
		if self.style=="tabs":
			tab = self.notebook.currentWidget()
			if tab!=None:
				tab.name=tab.get_json_obj().name
				return True,tab
		elif self.style=="list":
			sel=self.notebook.selectedItems()
			if len(sel)==1:
				sel=sel[0]
				sel.uid=self.get_obj_from_name(sel.text()).id
				sel.name=sel.text()
				return True,sel
		return False,None
 
	def get_obj_from_name(self,name):
		data=self.get_json_obj()
		for sim in data.segments:
			if sim.name==name:
				return sim
		return None

	def update_interface(self):
		data=self.get_json_obj()
		found,tab = self.get_current_item()
		
		if found==True:
			if self.style=="tabs":
				self.status_bar.showMessage(sim_paths.get_sim_path()+","+tab.get_json_obj().name+", segment"+str(data.segments.index(tab.get_json_obj())))
				self.tab_bar.obj_search_path=self.json_search_path
				self.tab_bar.obj_id=tab.uid
			if self.style=="list":
				item=self.get_obj_from_name(tab.text())
				if item!=None:
					self.status_bar.showMessage(sim_paths.get_sim_path()+","+item.name)

			self.ribbon.tb_clone.setEnabled(True)
			self.ribbon.tb_rename.setEnabled(True)
			self.ribbon.tb_delete.setEnabled(True)
		else:
			self.ribbon.tb_clone.setEnabled(False)
			self.ribbon.tb_rename.setEnabled(False)
			self.ribbon.tb_delete.setEnabled(False)

	def get_json_obj(self):
		return eval(self.json_search_path)

	def do_paste(self):
		exec("from "+self.name_of_tab_class+" import "+self.name_of_tab_class)
		data=json_root()
		data=self.get_json_obj()
		a=copy.deepcopy(data.segment_examples[0])
		a.load_from_json(self.tab_bar.paste_data)
		a.update_random_ids()
		data.segments.append(a)
		tab=eval(self.name_of_tab_class+"(data.segments[-1])")
		tab.uid=a.id
		self.notebook.addTab(tab,data.segments[-1].name)
		self.changed.emit()

	def callback_tab_moved(self,from_pos,to_pos):
		data=json_root()
		segments=self.get_json_obj().segments
		segments.insert(to_pos, segments.pop(from_pos))
		data.save()

	def on_item_activated(self,item):
		text=item.text()
		exec("from "+self.name_of_tab_class+" import "+self.name_of_tab_class)

		obj=self.get_obj_from_name(text)
		if obj!=None:
			self.tab=eval(self.name_of_tab_class+"(obj)")
			self.tab.uid=obj.id
			self.tab.show()

	def callback_menu(self,event):
		menu = QMenu(self)
		#selected=self.get_current_item()
		#if
		newAction = menu.addAction(icon_get("document-new"),_("New"))
		newAction.triggered.connect(self.callback_add_page)

		deleteAction = menu.addAction(icon_get("edit-delete"),_("Delete file"))
		deleteAction.triggered.connect(self.callback_delete_page)

		renameAction = menu.addAction(icon_get("rename"),_("Rename"))
		renameAction.triggered.connect(self.callback_rename_page)

		cloneAction = menu.addAction(icon_get("edit-copy"),_("Clone object"))
		cloneAction.triggered.connect(self.callback_clone_page)

		#menu.addSeparator()

		#cloneAction = menu.addAction(icon_get("edit-copy"),_("Copy json"))
		#cloneAction.triggered.connect(self.callback_clone_page)

		#cloneAction = menu.addAction(icon_get("edit-paste"),_("Paste json"))
		#cloneAction.triggered.connect(self.callback_clone_page)

		action = menu.exec_(self.mapToGlobal(event))

