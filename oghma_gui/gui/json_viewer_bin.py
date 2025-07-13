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

## @package json_viewer
#  This is the equivlent of the inp_viewer for json files
#


import os

from token_lib import tokens
from undo import undo_list_class
from util import latex_to_html
from gtkswitch import gtkswitch
from leftright import leftright
from g_select import g_select
from g_select_from_db import g_select_filter, g_select_shape, g_select_material, g_select_cache, g_select_morphology
from icon_widget import icon_widget

from gQtCore import gSignal
from PySide2.QtWidgets import  QApplication, QMenu, QSpacerItem
from PySide2.QtWidgets import QTextEdit,QWidget, QScrollArea,QVBoxLayout,QLabel,QHBoxLayout,QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,QComboBox,QGridLayout,QLineEdit, QSpinBox
from gQtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QIcon

from QComboBoxLang import QComboBoxLang
from QColorPicker import QColorPicker
from QColorPicker import QColorPicker_one_line

from gQtCore import QTimer

import i18n
_ = i18n.language.gettext

import functools
from generic_switch import generic_switch
from mobility_widget import mobility_widget
from g_select import g_select_electrical_edit

from QChangeLog import QChangeLog
from QLabel_click import QLabel_click
from gui_util import widget_get_value
from gui_util import widget_set_value

from QComboBoxLayers import QComboBoxLayers
from QComboBoxOpenCL import QComboBoxOpenCL
from icon_lib import icon_get
import json
from inp import inp
from decimal import Decimal
from sim_name import sim_name
from error_dlg import error_dlg
from gui_util import yes_no_dlg
from edit_with_units import edit_with_units

class tab_line(QWidget):
	changed = gSignal(str)

	def __init__(self):
		QWidget.__init__(self)
		self.token=""
		self.label=None
		self.edit_box=None
		self.units=None
		self.widget=""
		self.hide_on_token_eq=None
		self.show_on_token_eq=None
		self.pack_widget=None
		self.visible=True
		self.want_visible=False

	def callback_changed(self):
		self.changed.emit(self.token)

class json_viewer_bin(QWidget):

	changed = gSignal(str)

	#jason path is a string
	def __init__(self,data,db_json_file=None,db_json_db_path=None):
		QWidget.__init__(self)

		self.editable=True
		self.widget_list=[]
		self.tab=QGridLayout()

		self.setLayout(self.tab)

		self.json_default_values=None
		self.db_json_file=db_json_file
		self.db_json_db_path=db_json_db_path
		self.json_path=None

		self.menu_build()
		self.bin=data

	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			self.main_menu.exec_(event.globalPos())

	def get_easy_value(self,m):
		self.refind_json_path()
		val=self.bin.get_token_value(self.json_path,m)

		if m=="shape_dos":
			val=self.bin.get_token_value(self.json_path+".shape_dos","enabled")
		elif m=="shape_electrical":
			val=self.bin.get_token_value(self.json_path+".shape_electrical","enabled")
		elif type(val)==float:
			if val==0.0:
				return "0.0"
			if val<100 and val>0.01:
				return str(val)
			else:
				number=str(Decimal(str(val)).normalize()).replace("+","").replace("E","e")
				return number
		elif type(val)==int:
			return str(val)

		return val

	def menu_build(self):
		self.main_menu = QMenu(self)

		self.copy_menu=self.main_menu.addMenu(_("Copy"))

		action=self.copy_menu.addAction(icon_get("edit-copy"),_("Copy as JSON"))
		action.triggered.connect(self.do_copy)

		action=self.copy_menu.addAction(icon_get("edit-copy"),_("Copy json/python path"))
		action.triggered.connect(self.do_copy_path)

		action=self.copy_menu.addAction(icon_get("edit-copy"),_("Copy ObjID"))
		action.triggered.connect(self.do_copy_id)

		action=self.copy_menu.addAction(icon_get("edit-copy"),_("Copy as LaTex"))
		action.triggered.connect(self.do_copy_latex)

		action=self.copy_menu.addAction(icon_get("edit-copy"),_("Copy as csv"))
		action.triggered.connect(self.do_copy_as_csv)

		action=self.main_menu.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.do_paste)


		if self.db_json_file!=None:
			action=self.main_menu.addAction(icon_get("edit-undo"),_("Reimport from database"))
			action.triggered.connect(self.callback_reimport)

	def do_copy(self):
		self.refind_json_path()
		lines=self.bin.gen_json(self.json_path)
		lines[0]="\"data\": "+lines[0].split(":")[1]
		all_data=[]
		all_data.append("{")
		all_data.append("\"data_type\": \"\",")

		all_data.extend(lines)
		all_data.append("}")

		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText("\n".join(all_data), mode=cb.Clipboard)

	def do_copy_path(self):
		if self.uid!=None:
			self.refind_json_path()
			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText(self.json_path, mode=cb.Clipboard)

	def do_copy_latex(self):
		self.refind_json_path()
		latex_data=self.bin.dump_as_latex(self.json_path,tokens().get_fast_lib())

		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(latex_data, mode=cb.Clipboard)

	def do_copy_id(self):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(self.uid, mode=cb.Clipboard)

	def do_copy_as_csv(self):
		all_data=[]
		my_token_lib=tokens()
		self.refind_json_path()
		for token in self.bin.get_tokens_from_path(self.json_path):
			result=my_token_lib.find_json(token)
			if result!=False:
				units=result.units
				text_info=result.info
				val=self.bin.get_token_value(self.json_path,token)
				line=text_info+","+str(val)+","+units
				all_data.append(line)
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText("\n".join(all_data), mode=cb.Clipboard)

	def do_paste(self):
		self.refind_json_path()
		lines = QApplication.clipboard().text()
		read_data=json.loads(lines)
		paste_data=read_data['data']
		clip_data=json.dumps(paste_data)
		self.bin.import_json_to_obj(self.json_path,clip_data)

		self.update_values()
		self.bin.save()

	def callback_reimport(self):
		if self.db_json_file!=None:
			if yes_no_dlg(self,_("Are you sure you want reimport the material values from:")+" "+self.db_json_file)==True:
				self.f=inp()
				if self.f.load_json(self.db_json_file)!=False:
					self.json_default_values=json_get_val(self.f.json,self.db_json_db_path)
				else:
					error_dlg(self,_("File not found:")+" "+self.db_json_file)
					return

				self.refind_json_path()
				for token in self.bin.get_tokens_from_path(self.json_path):
					if token in self.json_default_values:
						val_from_db=self.json_default_values[token]
						self.bin.set_token_value(self.json_path,token,val_from_db)
				self.update_values()
				self.bin.save()

	def refind_json_path(self):
		if self.uid==None:
			self.json_path=self.json_root_path
		else:
			self.json_path=self.bin.find_path_by_uid(self.json_root_path,self.uid)
		if self.json_postfix!=None:
			self.json_path=self.json_path+"."+self.json_postfix

	def populate(self,json_root_path,uid=None,json_postfix=None):
		self.uid=uid
		self.json_root_path=json_root_path
		self.json_postfix=json_postfix
		pack_vars=[]
		pack_layout=None
		self.refind_json_path()
		my_token_lib=tokens()
		widget_number=0
		all_tokens=[]
		all_tokens=self.bin.get_tokens_from_path(self.json_path)
		#print(self.json_path)
		for token in all_tokens:
			a=tab_line()
			draw_widget=True

			show=False
			units="Units"

			result=my_token_lib.find_json(token)

			if result!=False:
				units=result.units
				text_info=result.info
				show=True
				if result.hidden==True:
					show=False
			

			description=None
			if show == True:
				#print(result,token,result.defaults)
				if pack_vars==[]:
					description=QLabel_click()
					description.setText(latex_to_html(text_info))
					description.clicked_dbl.connect(functools.partial(self.callback_ref,token,description,"edit"))
					description.main_menu=QMenu(self)

					if self.bin.is_token(self.json_path,"bib_"+token)==True:
						action=description.main_menu.addAction(icon_get("edit-copy"),_("Edit reference"))
						action.triggered.connect(functools.partial(self.callback_ref,token,description,"edit"))

						action=description.main_menu.addAction(icon_get("edit-copy"),_("Delete reference"))
						action.triggered.connect(functools.partial(self.callback_ref,token,description,"delete"))
						description.setStyleSheet('color: green')
					else:
						action=description.main_menu.addAction(icon_get("edit-copy"),_("Add reference"))
						action.triggered.connect(functools.partial(self.callback_ref,token,description,"edit"))

				unit=None
				#units widget
				if result.units_widget=="QLabel":
					if pack_vars==[]:
						unit=QLabel()
						unit.setText(latex_to_html(units))
				elif result.units_widget=="QPushButton":
					unit=QPushButton()
					unit.setText(latex_to_html(units))
					unit.setMinimumSize(50, 25)

				#edit widget
				if result.widget=="gtkswitch":
					a.edit_box=gtkswitch()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				if result.widget=="QSpinBox":
					a.edit_box=QSpinBox()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.setMaximum(1e6)
					a.edit_box.valueChanged.connect(a.callback_changed)
				elif result.widget=="leftright":
					a.edit_box=leftright()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select":
					a.edit_box=g_select()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.edit.textChanged.connect(a.callback_changed)
				elif result.widget=="g_select_material":
					a.edit_box=g_select_material()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select_filter":
					a.edit_box=g_select_filter()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select_shape":
					a.edit_box=g_select_shape()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select_cache":
					a.edit_box=g_select_cache()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select_morphology":
					a.edit_box=g_select_morphology()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="icon_widget":
					a.edit_box=icon_widget()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)

				elif result.widget=="QLineEdit":
					a.edit_box=QLineEdit()
					a.edit_box.setMinimumSize(75, 25)
					if self.editable==False:
						a.edit_box.setReadOnly(True)

					#a.edit_box.textChanged.connect(functools.partial())
					a.edit_box.textChanged.connect(a.callback_changed)

					#a.edit_box.show()
				elif result.widget=="QColorPicker":
					self.refind_json_path()
					r=self.bin.get_token_value(self.json_path,"color_r")
					g=self.bin.get_token_value(self.json_path,"color_g")
					b=self.bin.get_token_value(self.json_path,"color_b")
					alpha=self.bin.get_token_value(self.json_path,"color_alpha")
					a.edit_box=QColorPicker(r,g,b,alpha)
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="QColorPicker_one_line":
					self.refind_json_path()
					vals=self.bin.get_token_value(self.json_path,token)
					a.edit_box=QColorPicker_one_line()
					a.edit_box.setText(vals)
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.token=="fit_against":
					a.edit_box=QComboBoxLang()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.addItemLang("self",_("This simulation"))
					segments=self.bin.get_token_value("fits.fits","segments")
					for data_set in range(0,segments):
						fit_name=self.bin.get_token_value("fits.fits.segment"+str(data_set),"name")
						a.edit_box.addItemLang(fit_name,fit_name)

					a.edit_box.currentIndexChanged.connect(a.callback_changed)
				elif result.widget=="QComboBoxLang":
					a.edit_box=QComboBoxLang()
					a.edit_box.setMinimumSize(150, 25)
					if result.defaults!=None:
						for i in range(0,len(result.defaults)):
							a.edit_box.addItemLang(result.defaults[i][0],result.defaults[i][1])
								#widget=None,unit=None,token_class=None

					a.edit_box.currentIndexChanged.connect(a.callback_changed)
				elif result.widget=="QComboBoxLayers":
					a.edit_box=QComboBoxLayers()
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.currentIndexChanged.connect(a.callback_changed)
				elif result.widget=="QComboBoxOpenCL":
					a.edit_box=QComboBoxOpenCL()
					a.edit_box.setMinimumSize(150, 25)
				elif result.widget=="QChangeLog":
					a.edit_box=QChangeLog(self)
					a.edit_box.setMinimumHeight(100)
					if self.editable==False:
						a.edit_box.setReadOnly(True)
					a.edit_box.textChanged.connect(a.callback_changed)
				elif result.widget=="generic_switch":
					a.edit_box=generic_switch(state0=result.defaults[0][0],state1=result.defaults[1][0],state0_value=result.defaults[0][1],state1_value=result.defaults[1][1],)
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="mobility_widget":
					a.edit_box=mobility_widget(electrons=result.defaults[0])
					a.edit_box.setMinimumSize(400, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="g_select_electrical_edit":
					a.edit_box=g_select_electrical_edit(uid)
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
				elif result.widget=="edit_with_units":
					a.edit_box=edit_with_units()
					a.edit_box.token=result.token
					a.edit_box.setMinimumSize(150, 25)
					a.edit_box.changed.connect(a.callback_changed)
					#unit.setText("")
					unit=None
				elif result.widget=="QComboBox":
					a.edit_box=QComboBox()
					a.edit_box.setMinimumSize(150, 25)
					for i in range(0,len(result.defaults)):
						a.edit_box.addItem(result.defaults[i])
					
					a.edit_box.currentIndexChanged.connect(a.callback_changed)

				if a.edit_box!=None:
					a.changed.connect(self.callback_edit)

		

				if type(unit)==QPushButton:
					unit.clicked.connect(functools.partial(self.callback_unit_click,token,a.edit_box,unit))

				if draw_widget==True:
					#print(token,result.widget)
					a.token=token
					a.label=description
					a.units=unit
					a.widget=result.widget
					a.hide_on_token_eq=result.hide_on_token_eq
					a.show_on_token_eq=result.show_on_token_eq

					if len(pack_vars)==0 or result.pack!=[]:
						#print("description=",token,description,widget_number,pack_vars,result.pack)
						self.tab.addWidget(description,widget_number,0)
						if unit!=None:
							self.tab.addWidget(unit,widget_number,2)

					if result.pack!=[]:
						description.setText(latex_to_html(result.pack[0]))
						pack_widget=QWidget()
						a.pack_widget=pack_widget
						self.tab.addWidget(pack_widget,widget_number,1)
						pack_layout=QHBoxLayout()
						pack_layout.setSpacing(0)
						pack_layout.setMargin(0)
						pack_layout.setContentsMargins(2, 0, 2, 0)
						pack_widget.setLayout(pack_layout)
						pack_vars=result.pack[1:]

					if len(pack_vars)>0:
						val=" "+pack_vars[0]
						val=val+": "
						label=QLabel(val)
						pack_layout.addWidget(label)
						if len(pack_vars[0])<3:
							label.setMinimumWidth(25)
						else:
							label.adjustSize()
						pack_layout.addWidget(a.edit_box)
						pack_vars.pop(0)
					else:
						if a.edit_box!=None:
							self.tab.addWidget(a.edit_box,widget_number,1)
						

					
					self.widget_list.append(a)										
					widget_number=widget_number+1
		spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.tab.addItem(spacer, widget_number, 0)
		self.update_values()
		self.hide_show_widgets()

	def update_values(self):
		#print("asad")
		#import traceback
		#traceback.print_stack()
		self.refind_json_path()
		for item in self.widget_list:
			w=item.edit_box
			if self.bin.is_token(self.json_path,"bib_"+item.token)==True:
				if item.label!=None:
					item.label.setStyleSheet('color: green')
			else:
				if item.label!=None:
					item.label.setStyleSheet('color: black')

			if w!=None:
				w.blockSignals(True)
				value=self.get_easy_value(item.token)
				#print(self.json_path,item.token)
				if type(item.edit_box)==generic_switch:
					if value=="exponential":
						item.units.setEnabled(False)
					else:
						item.units.setEnabled(True)
				elif item.widget=="mobility_widget":
					
					if item.token=="symmetric_mobility_e":
						value = []
						value.append(self.bin.get_token_value(self.json_path,"symmetric_mobility_e"))
						value.append(self.bin.get_token_value(self.json_path,"mue_z"))
						value.append(self.bin.get_token_value(self.json_path,"mue_x"))
						value.append(self.bin.get_token_value(self.json_path,"mue_y"))
					if item.token=="symmetric_mobility_h":
						value = []
						value.append(self.bin.get_token_value(self.json_path,"symmetric_mobility_h"))
						value.append(self.bin.get_token_value(self.json_path,"muh_z"))
						value.append(self.bin.get_token_value(self.json_path,"muh_x"))
						value.append(self.bin.get_token_value(self.json_path,"muh_y"))

					if item.token=="electrical_symmetrical_resistance":
						value = []
						value.append(self.bin.get_token_value(self.json_path,"electrical_symmetrical_resistance"))
						value.append(self.bin.get_token_value(self.json_path,"electrical_series_z"))
						value.append(self.bin.get_token_value(self.json_path,"electrical_series_x"))
						value.append(self.bin.get_token_value(self.json_path,"electrical_series_y"))

				elif type(item.edit_box)==edit_with_units:
					new_token=item.edit_box.token
					value=self.get_easy_value(new_token)
					unit=self.bin.get_token_value(self.json_path,new_token+"_u")
					value=[value,unit]
				#print(item.token)
				widget_set_value(item.edit_box,value)

				w.blockSignals(False)



	def callback_unit_click(self,token,widget,unit):
		self.refind_json_path()
		if type(widget)==g_select_electrical_edit:
			from tab import tab_class
			name=self.bin.get_token_value(self.json_path,"name")
			self.window=tab_class(self.json_path+".shape_dos")
			self.window.setWindowTitle(_("Electrical parameter editor for shape")+" "+name+sim_name.web) 
			self.window.show()

		if type(widget)==g_select_material:
			widget.callback_button_click()

		if type(widget)==g_select_shape:
			widget.callback_button_click()

		if type(widget)==g_select_cache:
			widget.callback_button_click()

		if type(widget)==g_select_morphology:
			widget.callback_button_click()

		if type(widget)==icon_widget:
			widget.callback_button_click()


		if token=="dostype":
			from dos_editor import dos_editor
			self.dos_editor=dos_editor(self.json_path,self.uid)
			self.dos_editor.show()


	def hide_show_widgets(self):
		self.refind_json_path()
		for w in self.widget_list:
			w.want_visible=True

		for w in self.widget_list:
			if w.hide_on_token_eq!=None:	
				for token,val in w.hide_on_token_eq:
					if token.count(".")==0:
						json_val=self.bin.get_token_value(self.json_path,token)
					else:
						part1,part2 = token.rsplit('.',1)
						json_val=self.bin.get_token_value(self.json_path+"."+part1,part2)
					if str(json_val).lower()==str(val).lower():
						w.want_visible=False

			if w.show_on_token_eq!=None:
				do_hide=True
				found=False
				for val in w.show_on_token_eq:
					json_val=self.bin.get_token_value(self.json_path,val[0])
					if json_val!=None:
						found=True
					if str(json_val).lower()==str(val[1]).lower():
						do_hide=False

				if do_hide==True and found==True:
					w.want_visible=False

		for w in self.widget_list:
			if w.visible!=w.want_visible:
				w.visible=w.want_visible
				if w.edit_box!=None:
					w.edit_box.setVisible(w.visible)
				if w.units!=None:
					w.units.setVisible(w.visible)
				if w.label!=None:
					w.label.setVisible(w.visible)
				if w.pack_widget!=None:
					w.pack_widget.setVisible(w.visible)

	def callback_edit(self,token):
		for w in self.widget_list:
			if w.token==token:
				val=widget_get_value(w.edit_box)
				widget=w.edit_box
				unit=w.units

				if val!=None:
					if token.startswith("symmetric_mobility_e")==True:
						self.bin.set_token_value(self.json_path,"symmetric_mobility_e",val[0])
						self.bin.set_token_value(self.json_path,"mue_z",val[1])
						self.bin.set_token_value(self.json_path,"mue_x",val[2])
						self.bin.set_token_value(self.json_path,"mue_y",val[3])
					elif token.startswith("symmetric_mobility_h")==True:
						self.bin.set_token_value(self.json_path,"symmetric_mobility_h",val[0])
						self.bin.set_token_value(self.json_path,"muh_z",val[1])
						self.bin.set_token_value(self.json_path,"muh_x",val[2])
						self.bin.set_token_value(self.json_path,"muh_y",val[3])
					elif token.startswith("electrical_symmetrical_resistance")==True:
						self.bin.set_token_value(self.json_path,"electrical_symmetrical_resistance",val[0])
						self.bin.set_token_value(self.json_path,"electrical_series_z",val[1])
						self.bin.set_token_value(self.json_path,"electrical_series_x",val[2])
						self.bin.set_token_value(self.json_path,"electrical_series_y",val[3])	
					elif token.startswith("color_r")==True:
						self.bin.set_token_value(self.json_path,"color_r",widget.r)
						self.bin.set_token_value(self.json_path,"color_g",widget.g)
						self.bin.set_token_value(self.json_path,"color_b",widget.b)
						self.bin.set_token_value(self.json_path,"color_alpha",widget.alpha)
					elif type(widget)==g_select_electrical_edit:
						val=widget_get_value(widget)
						unit.setEnabled(val)
						self.bin.set_token_value(self.json_path,"shape_dos",val)
					elif type(widget)==edit_with_units:
						new_token=widget.token
						val=widget_get_value(widget)
						self.bin.set_token_value(self.json_path,new_token,val[0])
						self.bin.set_token_value(self.json_path,new_token+"_u",val[1])
					else:
						self.bin.set_token_value(self.json_path,token,val)
						
					if token=="dostype":
						if widget_get_value(widget)=="complex":
							unit.setEnabled(True)
						else:
							unit.setEnabled(False)


		self.hide_show_widgets()
		self.changed.emit(token)

	def set_edit(self,editable):
		self.editable=editable

	def callback_ref(self,token,widget,action_type):
		show=False
		ref_token="bib_"+token
		if action_type=="delete":
			self.bin.json_delete_token_using_path(self.json_path, ref_token)
			self.changed.emit(token)
		elif action_type=="edit":
			if self.bin.is_token(self.json_path,ref_token)==True:
				show=True
			else:
				self.bin.add_bib_item(self.json_path,ref_token)
				self.changed.emit(token)
				show=True
			
			
		self.update_values()

		if show==True:
			from config_window import class_config_window
			self.window_bib=class_config_window([self.json_path+"."+ref_token],[_("Reference")],title=_("Bibliography editor"),icon="ref")
			self.window_bib.show()
		


