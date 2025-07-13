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

#tabs - thse are so compiled windows versions have the tabs already loaded
from time_domain_experiment_tab import time_domain_experiment_tab
from tab_light_src import tab_light_src
from tab_probes import tab_probes
from tab_jv import tab_jv
from tab_light_src import tab_light_src
from cluster_tab import cluster_tab
from tab_ml import tab_ml
from fxexperiment_tab import fxexperiment_tab

from QHTabBar import QHTabBar
from gui_util import yes_no_dlg
from gQtCore import gSignal
from util import wrap_text
from QWidgetSavePos import QWidgetSavePos
from css import css_apply

from progress_class import progress_class
from process_events import process_events

from ribbon_experiment import ribbon_experiment
import copy
from global_objects import global_object_run
from cal_path import sim_paths
from json_c import json_local_root
from json_c import json_tree_c
import json

class experiment_bin(QWidgetSavePos):

	changed = gSignal()
	sub_tab_changed = gSignal(str)
	delete_item = gSignal(str)
	rename_item = gSignal(str,str)

	def __init__(self,name_of_tab_class,window_save_name="time_domain_experiment", window_title=_("Time domain experiment window"),json_search_path=None,icon="icon",style="tabs",min_y=700,display_the_toolbar=True,custon_ribbon=None,uid=None, json_config_postfix=None, add_notebook_in_tab=False,json_template="oghma_save_file"):
		QWidgetSavePos.__init__(self,window_save_name)
		if json_template=="oghma_save_file":
			self.bin=json_tree_c()
		elif json_template=="oghma_local":
			self.bin=json_local_root()

		self.main_vbox = QVBoxLayout()
		self.json_root_path=json_search_path
		self.json_postfix=None
		self.name_of_tab_class=name_of_tab_class
		self.setMinimumSize(800, min_y)
		self.setWindowTitle2(window_title)
		self.setWindowIcon(icon_get(icon))
		self.style=style
		self.uid=uid
		self.refind_json_path()
		self.json_config_postfix=json_config_postfix
		if display_the_toolbar==True:
			if custon_ribbon==None:
				self.ribbon=ribbon_experiment()
			else:
				self.ribbon=custon_ribbon

			self.main_vbox.addWidget(self.ribbon)

		else:
			#build the components but don't add them
			self.ribbon=ribbon_experiment()

		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


		if self.style=="tabs":
			self.notebook = QTabWidget()
			css_apply(self.notebook ,"style_h.css")
			self.tab_bar=QHTabBar()
			self.tab_bar.bin=json_tree_c()
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

		if add_notebook_in_tab==False:
			self.main_vbox.addWidget(self.notebook)
		else:
			self.h_notebook = QTabWidget()
			self.h_notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			#css_apply(self.h_notebook,"style_h.css")
			self.h_notebook.addTab(self.notebook,_("Data sets"))
			self.main_vbox.addWidget(self.h_notebook)

		self.status_bar=QStatusBar()
		if display_the_toolbar==True:
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

	def refind_json_path(self):
		if self.uid==None:
			self.json_path=self.json_root_path
		else:
			self.json_path=self.bin.find_path_by_uid(self.json_root_path,self.uid)
			print("found:",self.json_path)

		if self.json_postfix!=None:
			self.json_path=self.json_path+".".self.json_postfix

	def make_new_tab(self,uid):
		exec("from "+self.name_of_tab_class+" import "+self.name_of_tab_class)
		if self.json_config_postfix==None:
			options=""
		else:
			options=",json_postfix=\""+self.json_config_postfix+"\""
		
		tab=eval(self.name_of_tab_class+"(self.json_path,uid"+options+")")
		return tab

	def load_tabs(self):
		self.refind_json_path()

		if self.style=="tabs":
			i=0
			progress_window=progress_class()
			progress_window.show()
			progress_window.start()

			process_events()

			segments=self.bin.get_token_value(self.json_path,"segments")
			name_update=False
			for i in range(0,segments):
				seg_path=self.json_path+".segment"+str(i)
				uid=self.bin.get_token_value(seg_path,"id")
				name=self.bin.get_token_value(seg_path,"name")

				if name=="none":			#compat layer remove Dec 2026
					name=self.bin.get_token_value(seg_path+".config","fit_name")
					self.bin.set_token_value(seg_path,"name",name)
					name_update=True
				print(uid)
				tab=self.make_new_tab(uid)
				tab.uid=uid
				self.add_tab(tab,name)

				progress_window.set_fraction(float(i)/float(segments))
				progress_window.set_text(_("Loading")+" "+name)
				process_events()

			progress_window.stop()
			if name_update==True:
				self.bin.save()

		else:
			self.notebook.clear()
			self.refind_json_path()

			segments=self.bin.get_token_value(self.json_path,"segments")
			for i in range(0,segments):
				name=self.bin.get_token_value(self.json_path+".segment"+str(i),"name")
				enabled=self.bin.get_token_value(self.json_path+".segment"+str(i),"enabled")
				icon=self.bin.get_token_value(self.json_path+".segment"+str(i),"icon")
				itm = QListWidgetItem(name)
				if icon!=None:
					if enabled==None:
						a=icon_get(icon)
					else:
						a=icon_get(icon,grey_scale=not enabled)

					itm.setIcon(a)
				self.notebook.addItem(itm)

		
		self.update_interface()


	def update(self):
		for i in range(0,self.notebook.count()):
			w=self.notebook.widget(i)
			w.update()

	def callback_sub_tab_changed(self,tab_name):
		self.sub_tab_changed.emit(tab_name)

	def add_tab(self,tab,name):
		self.notebook.addTab(tab,name)
		try:
			tab.tab_changed.connect(self.callback_sub_tab_changed)
		except:
			pass

	def clear_pages(self):
		self.notebook.clear()

	def callback_rename_page(self):
		found,tab_path = self.get_current_item()
		if found==True:
			old_sim_name=self.bin.get_token_value(tab_path,"name")
			new_sim_name=dlg_get_text2( _("Rename:"), old_sim_name,"rename.png")

			new_sim_name=new_sim_name.ret
			
			if new_sim_name!=None:
				self.bin.set_token_value(tab_path,"name",new_sim_name)

				if self.style=="tabs":
					self.notebook.setTabText(self.notebook.currentIndex(), new_sim_name)
				else:
					self.load_tabs()

				self.bin.save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()
				self.rename_item.emit(old_sim_name,new_sim_name)

	def callback_clone_page(self):
		found,tab_path = self.get_current_item()
		if found==True:
			old_sim_name=self.bin.get_token_value(tab_path,"name")
			new_sim_name=dlg_get_text2( _("Clone:"), old_sim_name+"_new","clone.png")

			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				root_path, src_segment = tab_path.rsplit('.', 1)
				new_segment_path=self.bin.clone_segment(root_path,src_segment,new_sim_name)
				if self.fixup_new!=None:
					self.fixup_new(new_segment_path)

				uid=self.bin.get_token_value(new_segment_path,"id")

				if self.style=="tabs":
					tab=self.make_new_tab(uid)
					tab.uid=uid
					self.add_tab(tab,new_sim_name)
				else:
					self.load_tabs()
				self.bin.save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()

	def callback_delete_page(self):
		found, tab_path = self.get_current_item()
		if found==True:
			old_sim_name=self.bin.get_token_value(tab_path,"name")
			response=yes_no_dlg(self,_("Are you sure you want to delete : ")+old_sim_name.replace("\n"," "))
			if response == True:
				index=self.notebook.currentIndex()
				path, seg = tab_path.rsplit('.', 1)
				self.bin.delete_segment(path,seg)
				if self.style=="tabs":
					self.notebook.removeTab(index)
				else:
					self.load_tabs()
				self.bin.save()
				global_object_run("ribbon_sim_mode_update")
				self.changed.emit()

				self.delete_item.emit(old_sim_name)

	def callback_add_page(self):
		found,tab_path = self.get_current_item()
		if found==True:
			old_sim_name=self.bin.get_token_value(tab_path,"name")
			new_name=old_sim_name+"_new"
		else:
			new_name="new"

		new_sim_name=dlg_get_text2( _("Make a new:"), new_name,"document-new.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:

			path_of_new_tab=self.bin.make_new_segment(self.json_path,new_sim_name,-1)
			if self.fixup_new!=None:
				self.fixup_new(path_of_new_tab)

			if self.style=="tabs":
				uid=self.bin.get_token_value(path_of_new_tab,"id")
				tab=self.make_new_tab(uid)
				tab.uid=uid

				self.add_tab(tab,new_sim_name)
			else:
				self.load_tabs()

			self.bin.save()
			global_object_run("ribbon_sim_mode_update")
			self.changed.emit()

	def get_current_item(self):
		if self.style=="tabs":
			tab = self.notebook.currentWidget()
			if tab!=None:
				tab_path=self.bin.find_path_by_uid(self.json_root_path,tab.uid)
				return True,tab_path
		elif self.style=="list":
			sel=self.notebook.selectedItems()
			if len(sel)==1:
				sel=sel[0]
				tab_path=self.get_path_from_name(sel.text())
				uid=self.bin.get_token_value(tab_path,"id")
				return True,tab_path
		return False,None
 
	def get_path_from_name(self,name_to_find):
		segments=self.bin.get_token_value(self.json_path,"segments")
		for n in range(0,segments):
			path=self.json_path+".segment"+str(n)
			name=self.bin.get_token_value(path,"name")
			if name==name_to_find:
				return path

		return None

	def update_interface(self):
		found, tab_path = self.get_current_item()

		if found==True:
			name=self.bin.get_token_value(tab_path,"name")
			uid=self.bin.get_token_value(tab_path,"id")

			if self.style=="tabs":
				self.status_bar.showMessage(sim_paths.get_sim_path()+","+name+", "+tab_path.split(".")[-1])
				self.tab_bar.obj_search_path=self.json_root_path
				self.tab_bar.obj_id=uid
			if self.style=="list":
				self.status_bar.showMessage(sim_paths.get_sim_path()+","+name)

			self.ribbon.tb_clone.setEnabled(True)
			self.ribbon.tb_rename.setEnabled(True)
			self.ribbon.tb_delete.setEnabled(True)
		else:
			self.ribbon.tb_clone.setEnabled(False)
			self.ribbon.tb_rename.setEnabled(False)
			self.ribbon.tb_delete.setEnabled(False)

	def do_paste(self):
		clip_data=json.dumps(self.tab_bar.paste_data)

		path_of_new_tab=self.bin.make_new_segment(self.json_path,"tmp_name",-1)
		if self.fixup_new!=None:
			self.fixup_new(path_of_new_tab)
		
		self.bin.import_json_to_obj(path_of_new_tab,clip_data)
		uid=self.bin.get_token_value(path_of_new_tab,"id")
		tab=self.make_new_tab(uid)
		tab.uid=uid
		name=self.bin.get_token_value(path_of_new_tab,"name")
		self.add_tab(tab,name+"_new")
		self.bin.save()
		self.changed.emit()

	def callback_tab_moved(self,from_pos,to_pos):
		self.refind_json_path()
		self.bin.segments_swap(self.json_path,from_pos,to_pos)
		self.bin.save()

	def on_item_activated(self,item):
		text=item.text()
	
		tab_path=self.get_path_from_name(text)
		uid=self.bin.get_token_value(tab_path,"id")
		if tab_path!=None:
			#print(self.name_of_tab_class,obj)
			self.tab=self.make_new_tab(uid)
			self.tab.show()

	def callback_enable_disable(self):
		found,tab_path = self.get_current_item()
		if tab_path!=None:
			enabled=self.bin.get_token_value(tab_path,"enabled")
			if enabled!=None:
				enabled= not enabled
				self.bin.set_token_value(tab_path,"enabled",enabled)
				self.bin.save()
				self.load_tabs()

	def callback_menu(self,event):
		menu = QMenu(self)

		newAction = menu.addAction(icon_get("document-new"),_("New"))
		newAction.triggered.connect(self.callback_add_page)

		deleteAction = menu.addAction(icon_get("edit-delete"),_("Delete file"))
		deleteAction.triggered.connect(self.callback_delete_page)

		renameAction = menu.addAction(icon_get("rename"),_("Rename"))
		renameAction.triggered.connect(self.callback_rename_page)

		cloneAction = menu.addAction(icon_get("edit-copy"),_("Clone object"))
		cloneAction.triggered.connect(self.callback_clone_page)

		found,tab_path = self.get_current_item()

		if tab_path!=None:
			enabled=self.bin.get_token_value(tab_path,"enabled")

			if enabled!=None:
				if enabled==True:
					enabled = menu.addAction(icon_get("tick"),_("Enabled"))
				else:
					enabled = menu.addAction(icon_get("cross"),_("Disabled"))
				enabled.triggered.connect(self.callback_enable_disable)


		action = menu.exec_(self.mapToGlobal(event))

