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

## @package window_json_tree_view
#  Window to select a parameter to scan.
#


import i18n
_ = i18n.language.gettext

#qt
import os
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QSizePolicy,QTabWidget,QTableWidget,QAbstractItemView, QTreeWidget, QPushButton, QHBoxLayout, QTreeWidgetItem, QLabel, QLineEdit
from PySide2.QtGui import QPainter,QIcon
from PySide2.QtGui import QFont

from icon_lib import icon_get
from token_lib import tokens
from sim_name import sim_name
from gQtCore import gSignal
from json_c import json_tree_c
from token_lib import fast_lib
 
class obj_info:
	def __init__(self):
		self.token=None
		self.display_name=None
		self.pointer_to_var=None
		self.icon=None
		self.hidden=False
		self.bin=False

class window_json_tree_view(QWidget):

	double_click = gSignal()

	def __init__(self,language_mode="python",title=_("Explore the simulation data structure")):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.my_token_lib=tokens()
		self.human_path_col=0
		self.json_path_col=-1
		self.main_vbox=QVBoxLayout()
		self.save_function=None
		self.show_values=True
		self.language_mode=language_mode
		self.object_mode=""
		self.show_data_items=True
		self.disable_python_tree=False

		if language_mode=="python_json":
			self.setWindowIcon(icon_get("json_python"))
		elif language_mode=="matlab":
			self.setWindowIcon(icon_get("json_matlab"))
		else:
			self.setWindowIcon(icon_get("json_python"))

		self.setWindowTitle(title+" https://www.oghma-nano.com") 

		self.icon_var=icon_get("python_var")
		self.icon_class=icon_get("python_object")

		self.tab = QTreeWidget()

		self.font = QFont()
		self.font.setPointSize(int(20))
	
		self.tab.setFont(self.font)
		self.edit_box=QLineEdit()
		self.main_vbox.addWidget(self.edit_box)

		self.main_vbox.addWidget(self.tab)

		self.hwidget=QWidget()

		self.setLayout(self.main_vbox)
		self.english=False

		self.tab.header().close()
		self.tab.itemClicked.connect(self.callback_item_clicked)

		self.setMinimumSize(700,700)
		self.path_python=""
		self.update()
		self.tab.itemExpanded.connect(self.callback_expand)


	def join_dots(self, *args):
	    return ".".join(arg.strip(".") for arg in args if arg)

	def callback_item_clicked(self):
		self.update_path()
		self.double_click.emit()

	def json_decode_bin(self,path,pointer,depth):
		var_list=[]

		#bin
		tokens=json_tree_c().get_tokens_from_path(path)
		if tokens!=None:
			for token in tokens:
				a=obj_info()
				if token.endswith("_")==False:
					obj_path=self.join_dots(path,token)
					name=token
					if self.english==True:
						found=False
						if token.startswith("segment"):
							if self.bin.is_token(obj_path,"name")==True:
								name=self.bin.get_token_value(obj_path,"name")
								found=True
						if found==False:
							token_lib_item=self.my_token_lib.find_json(token)
							if token_lib_item!=False:
								name=token_lib_item.info
						

					a.token=token
					a.display_name=name
					a.bin=True
					
					if json_tree_c().is_node(obj_path)==False:
						a.icon=self.icon_var
					else:
						if json_tree_c().is_token(obj_path,"icon")==True:
							icon_name=json_tree_c().get_token_value(obj_path,"icon")
							a.icon=icon_get(icon_name)
						elif json_tree_c().is_token(obj_path,"icon_")==True:
							icon_name=json_tree_c().get_token_value(obj_path,"icon_")
							a.icon=icon_get(icon_name)
						else:
							a.icon=self.icon_class
					var_list.append(a)

		for o in var_list:
			if o.hidden==False:
				
				found=False
				for c in range(0,pointer.childCount()):
					if o.display_name==pointer.child(c).text(0):
						found=True
						pointer_next=pointer.child(c)
						break
				item=self.join_dots(path,o.token)
				if found==False:
					if json_tree_c().is_node(item)==False:
						#print(o.token,self.show_data_items)
						if self.show_data_items==True and o.token.endswith("_u")==False:
							pointer_next=QTreeWidgetItem(pointer, [o.display_name])
							pointer_next.setIcon(0,o.icon)
							if self.show_values==True:
								pointer_next=QTreeWidgetItem(pointer_next)
								item_value=json_tree_c().get_token_value(path,o.token)
								label=QLabel("value=<font color=\"green\">"+str(item_value)+"</font>")
								self.tab.setItemWidget(pointer_next, 0, label);
					else:
						pointer_next=QTreeWidgetItem(pointer, [o.display_name])

						pointer_next.setIcon(0,o.icon)

				#print(item,json_tree_c().is_node(item),depth)

				if json_tree_c().is_node(item)==True:
					if depth<1:
						self.json_decode_bin(item,pointer_next,depth+1)

				if depth>0:		#only add the first node so we get that arrow thing
					break


	def update(self):
		self.tab.clear()
		root = QTreeWidgetItem(self.tab, ["data"])
		root.setExpanded(True)
		root.setIcon(0,icon_get("tree"))
		self.json_decode_bin("",root,0)

	def callback_expand(self, item):
		found_in_python=False		
		path=self.get_json_path([item])
		if path=="data":
			return
		if path.startswith("data."):
			path=path[5:]
		if json_tree_c().is_token(path,"")==True:
			self.json_decode_bin(path,item,0)

		

	def get_path_from_selected(self,selected):
		if selected:
			item = selected[0]

			path = []
			while item is not None:
				path.append(str(item.text(0)))
				item = item.parent()
		path=list(reversed(path))
		return path

	def get_json_path(self,getSelected):						#This always returns a json path
		path=self.get_path_from_selected(getSelected)
		test=".".join(path)
		if test.startswith("data."):
			test=test[5:]
		else:
			return ""
		ret=self.bin.human_path_to_json(fast_lib,test)
		return ret

	def get_human_path(self,selected):
		json_path=self.get_json_path(selected)
		ret=self.bin.json_path_to_human_path(fast_lib,json_path)
		return ret

	def update_path(self):
		node = self.tab.selectedItems()
		self.path_python=self.get_json_path(node)
		self.edit_box.setText(self.path_python)


