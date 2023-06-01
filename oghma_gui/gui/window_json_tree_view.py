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
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QSizePolicy,QTabWidget,QTableWidget,QAbstractItemView, QTreeWidget, QPushButton, QHBoxLayout, QTreeWidgetItem, QLabel, QLineEdit
from PySide2.QtGui import QPainter,QIcon
from PySide2.QtGui import QFont

from icon_lib import icon_get
from json_root import json_root
from token_lib import tokens
from json_base import isclass
from sim_name import sim_name
from scan_human_labels import get_json_path_from_human_path
from scan_human_labels import get_python_path_from_human_path

class window_json_tree_view(QWidget):


	def __init__(self,language_mode="python"):
		QWidget.__init__(self)
		self.my_token_lib=tokens()
		self.human_path_col=0
		self.json_path_col=-1
		self.main_vbox=QVBoxLayout()
		self.save_function=None
		self.show_values=True
		self.language_mode=language_mode

		if language_mode=="python_json":
			self.setWindowIcon(icon_get("json_python"))
		elif language_mode=="matlab":
			self.setWindowIcon(icon_get("json_matlab"))
		else:
			self.setWindowIcon(icon_get("json_python"))

		self.setWindowTitle(_("Explore the simulation data structure")+sim_name.web_window_title) 

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
		self.tab.itemClicked.connect(self.update_path)

		self.setMinimumSize(700,700)
		self.update()
		self.tab.itemExpanded.connect(self.callback_expand)


	def json_decode(self,class_data,path,pointer,depth):
		class obj_info:
			def __init__(self):
				self.var_name=None
				self.pointer_to_var=None
				self.icon=None

		var_list=[]


		if "var_list" in dir(class_data):
			for v in class_data.var_list:
				a=obj_info()
				name=v[0]
				if name.endswith("_")==False:
					if self.english==True:
						token=self.my_token_lib.find_json(name)
						if token!=False:
							name=token.info
						try:
							name=dic[key]['name']
						except:
							pass
					a.var_name=name
					a.pointer_to_var=getattr(class_data, v[0])
					var_list.append(a)

		if "layers" in dir(class_data):
			for l in range(0,len(class_data.layers)):
				a=obj_info()
				name="layers["+str(l)+"]"
				if self.english==True:
					try:
						name=class_data.layers[l].name
					except:
						pass
				a.var_name=name
				a.pointer_to_var=class_data.layers[l]
				var_list.append(a)

		if "segments" in dir(class_data):
			for l in range(0,len(class_data.segments)):
				a=obj_info()
				name="segments["+str(l)+"]"
				if self.english==True:
					try:
						name=class_data.segments[l].name
					except:
						pass
				a.var_name=name
				a.pointer_to_var=class_data.segments[l]
				var_list.append(a)

		#find icons
		for o in var_list:
			if isclass(o.pointer_to_var)==False:
				o.icon=self.icon_var
			else:
				o.icon=self.icon_class
				if "icon" in dir(o.pointer_to_var):
					o.icon=icon_get(o.pointer_to_var.icon)
				elif "icon_" in dir(o.pointer_to_var):
					o.icon=icon_get(o.pointer_to_var.icon_)

		for o in var_list:
			found=False
			for c in range(0,pointer.childCount()):
				if o.var_name==pointer.child(c).text(0):
					found=True
					pointer_next=pointer.child(c)
					break
			item=path+"/"+o.var_name
			if found==False:
				if isclass(o.pointer_to_var)==False:
					pointer_next=QTreeWidgetItem(pointer, [o.var_name])
					pointer_next.setIcon(0,o.icon)
					if self.show_values==True:
						pointer_next=QTreeWidgetItem(pointer_next)
						label=QLabel("value=<font color=\"green\">"+str(o.pointer_to_var)+"</font>")
						self.tab.setItemWidget(pointer_next, 0, label);
				else:
					pointer_next=QTreeWidgetItem(pointer, [o.var_name])
					pointer_next.setIcon(0,o.icon)

			if isclass(o.pointer_to_var)==True:
				if depth<1:
					self.json_decode(o.pointer_to_var,item,pointer_next,depth+1)

			if depth>0:		#only add the first node so we get that arrow thing
				break

	def update(self):
		self.tab.clear()
		root = QTreeWidgetItem(self.tab, ["data"])
		root.setExpanded(True)
		data=json_root()
		self.json_decode(data,"",root,0)

	def callback_expand(self, item):
		
		#print(python_path)
		path=self.cal_path([item])
		if path=="data":
			return
		if path.startswith("data."):
			path=path[5:]
		python_path=get_python_path_from_human_path(json_root(),path)
		p=eval(python_path)
		self.json_decode(p,"",item,0)

	def get_path_from_selected(self,selected):
		if selected:
			item = selected[0]

			path = []
			while item is not None:
				path.append(str(item.text(0)))
				item = item.parent()
		path=list(reversed(path))
		return path

	def cal_path(self,getSelected,language="python"):
		path=self.get_path_from_selected(getSelected)

		if language=="python":
			ret=".".join(path)
		elif language=="human":
			ret="/".join(path)
			if ret.startswith("data/"):
				ret=ret[5:]
		elif language=="python_json":
			i=0
			ret="data"
			for obj in path:
				if i>0:
					ret=ret+"[\""+obj.replace("[","").replace("]","")+"\"]"
				i=i+1
		elif language=="matlab":
			ret=".".join(path).replace("[","").replace("]","")

		return ret

	def cal_json_path(self,selected):
		path=self.get_path_from_selected(selected)
		print(path)

	def update_path(self):
		node = self.tab.selectedItems()
		path_python=self.cal_path(node,language=self.language_mode)
		self.edit_box.setText(path_python)



