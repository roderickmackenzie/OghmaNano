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

## @package g_tab2_bin
#  A table widget
#


#qt
from gQtCore import QSize, Qt, gSignal
from PySide2.QtWidgets import QWidget,QPushButton,QToolBar, QVBoxLayout, QTableWidget,QAbstractItemView, QTableWidgetItem, QComboBox, QApplication, QLineEdit, QTextEdit, QAction, QMenu
from PySide2.QtGui import QCursor

from QComboBoxLang import QComboBoxLang
from QComboBoxFiles import QComboBoxFiles
from icon_lib import icon_get

from energy_to_charge import energy_to_charge
from gtkswitch import gtkswitch
from leftright import leftright
from g_applied_voltage import g_applied_voltage
from g_contact_type import g_majority_contact
from g_contact_type import g_minority_contact
from g_probe_type import g_probe_type
from g_select import g_select
from g_select_base import g_select_base
from tb_spectrum import tb_spectrum
from str2bool import str2bool
from token_lib import tokens
from tab_button import tab_button
from g_select import g_select, g_select_import
from g_select_from_db import g_select_filter, g_select_shape, g_select_material, g_select_morphology
from g_select_equation import g_select_equation
from edit_with_units import edit_with_units
from QComboBoxNetworkInputs import QComboBoxNetworkInputs
from QComboBoxNetworkOutputs import QComboBoxNetworkOutputs
from json_c import json_tree_c

class g_tab2_bin(QTableWidget):

	new_row_clicked = gSignal(int)
	changed = gSignal(str)

	def __init__(self,toolbar=None,json_bin=json_tree_c()):
		QTableWidget.__init__(self)
		self.bin=json_bin
		self.dir_path=None			#This is used if the widgets need to scan a directory
		self.json_root_path=None
		self.json_postfix=None		#This is used to point to another segments structure deeper than the root path
		self.uid=None
		self.json_tokens=[]
		self.override_widgets=None
		self.base_obj=None
		self.toolbar=toolbar
		self.check_enabled_callback=None
		self.disable_callbacks=False
		self.menu_disabled=False
		self.setSelectionBehavior(QAbstractItemView.SelectItems)
		self.SelectionMode (QAbstractItemView.SingleSelection)
		self.json_search_path=None

		if self.toolbar!=None:
			self.toolbar.setIconSize(QSize(32, 32))
			self.tb_add = QAction(icon_get("list-add"), _("Add"), self)
			self.toolbar.addAction(self.tb_add)
			self.tb_add.triggered.connect(self.callback_add_row)

			self.tb_remove = QAction(icon_get("list-remove"), _("Delete row"), self)
			self.toolbar.addAction(self.tb_remove)
			self.tb_remove.triggered.connect(self.callback_remove_rows)

			self.tb_down= QAction(icon_get("go-down"), _("Move down"), self)
			self.toolbar.addAction(self.tb_down)
			self.tb_down.triggered.connect(self.callback_move_down)

			self.tb_up= QAction(icon_get("go-up"), _("Move up"), self)
			self.toolbar.addAction(self.tb_up)
			self.tb_up.triggered.connect(self.callback_move_up)

		self.menu = QMenu(self)
		self.menu_copy = QAction(icon_get("edit-copy"),_("Copy"), self)
		self.menu_copy.triggered.connect(self.callback_menu_copy)
		self.menu.addAction(self.menu_copy)

		self.menu_paste = QAction(icon_get("edit-paste"),_("Paste"), self)
		self.menu.addAction(self.menu_paste)
		self.menu_paste.triggered.connect(self.callback_menu_paste)

		self.menu_delete = QAction(icon_get("list-remove"),_("Delete row"), self)
		self.menu.addAction(self.menu_delete)
		self.menu_delete.triggered.connect(self.callback_remove_rows)

		self.menu_move_up = QAction(icon_get("go-up"),_("Move up"), self)
		self.menu.addAction(self.menu_move_up)
		self.menu_move_up.triggered.connect(self.callback_move_up)

		self.menu_move_down = QAction(icon_get("go-down"),_("Move down"), self)
		self.menu.addAction(self.menu_move_down)
		self.menu_move_down.triggered.connect(self.callback_move_down)

		self.my_token_lib=tokens()
		self.verticalHeader().setVisible(False)
		self.cellChanged.connect(self.callback_value_changed)

		script=self.menu.addMenu(icon_get("script"),_("Script"))
		action=script.addAction(icon_get("edit-copy"),_("Copy path (json)"))
		action.triggered.connect(self.object_copy_path)

		self.callback_a=None
		self.fixup_new_row=None

	def callback_add_row(self):
		row=self.get_new_row_pos()
		json_path=self.refind_json_path()
		#print("adding at:",json_path)
		path_of_new_segment=self.bin.make_new_segment(json_path,"",row)
		self.insert_row(path_of_new_segment,row)
		self.new_row_clicked.emit(row)
		self.changed.emit("all")

	def object_copy_path(self):
		if self.rowCount()==0:
			return

		rows=self.selectionModel().selectedRows()

		for a in rows:
			row_number=a.row()
			break

		rows=self.selectionModel().selectedRows()
		ret=self.refind_json_path()+".segment"+str(row_number)
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(ret, mode=cb.Clipboard)

	def set_override_widgets(self,override_widgets):
		self.override_widgets=override_widgets

	def set_tokens(self,tokens,override_widgets=None):
		self.json_tokens=tokens
		self.blockSignals(True)
		self.clear()
		self.setColumnCount(len(self.json_tokens))

		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.blockSignals(False)

	def set_labels(self,labels):
		self.json_labels=labels
		self.setHorizontalHeaderLabels(self.json_labels)

	def insert_row(self,segment_path,y):
		x=0
		self.blockSignals(True)
		self.insertRow(y)
		for t in self.json_tokens:
			if t.count(".")>0:
				t=t.split(".")[-1]
			token=self.my_token_lib.find_json(t)
			added=False
			if token!=False:
				if self.override_widgets!=None:
					if self.override_widgets[x]!="":
						widget_name=self.override_widgets[x]
						item1=eval(widget_name+"()")
						self.setCellWidget(y,x, item1)
						added=True

				if added==False:
					if token.widget!="QLineEdit":
						widget_name=token.widget
						item1=eval(widget_name+"()")
						self.setCellWidget(y,x, item1)
						added=True

			if added==False:
				widget_name="none"
				item1 = QTableWidgetItem()
				if self.check_enabled_callback!=None:
					if self.check_enabled_callback(segment_path,t)==False:
						item1.setFlags(item1.flags() ^ Qt.ItemIsEnabled)
				self.setItem(y,x,item1)
			
			if widget_name=="QComboBoxLang":
				for i in range(0,len(token.defaults)):
					item1.addItemLang(token.defaults[i][0],token.defaults[i][1])
				item1.currentIndexChanged.connect(self.callback_value_changed)
			if widget_name=="QComboBox":
				item1.currentIndexChanged.connect(self.callback_value_changed)
			if widget_name=="QComboBoxFiles":
				item1.path=self.dir_path
				item1.update()
				item1.currentIndexChanged.connect(self.callback_value_changed)
			if widget_name=="QComboBoxNetworkInputs":
				item1.currentIndexChanged.connect(self.callback_value_changed)
			if widget_name=="QComboBoxNetworkOutputs":
				item1.changed.connect(self.callback_value_changed)
			elif widget_name=="g_probe_type":
				item1.changed.connect(self.callback_value_changed_direct)
			elif widget_name=="g_select":
				item1.edit.textChanged.connect(self.callback_value_changed)
				if self.callback_a!=None:
					item1.button.clicked.connect(self.callback_a)
			elif widget_name=="tb_spectrum":
				item1.currentIndexChanged.connect(self.callback_value_changed)
			elif widget_name=="QComboBoxFiles":
				item1.currentIndexChanged.connect(self.callback_value_changed)
			elif widget_name=="edit_with_units":
				item1.token=t
				item1.changed.connect(self.callback_value_changed)
			else:
				if hasattr(item1, "changed"):
					item1.changed.connect(self.callback_value_changed)

			x=x+1

		if self.fixup_new_row!=None:
			self.fixup_new_row(y)

		self.update_row(y)
		self.blockSignals(False)


	def update_row(self,y):
		root_path=self.refind_json_path()

		x=0
		for t in self.json_tokens:
			segment_path=root_path+".segment"+str(y)
			w=self.cellWidget(y, x)
			wt=type(w)
			if wt==edit_with_units:
				t=w.token
			units=self.bin.get_token_value(segment_path,t+"_u")
			value=self.bin.get_token_value(segment_path,t)
			uid=self.bin.get_token_value(segment_path,"id")
			#self.bin.dump()
			if wt==edit_with_units:
				unit=self.bin.get_token_value(segment_path,t+"_u")
				self.set_value(y,x,[value,units],uid)
			else:
				self.set_value(y,x,str(value),uid)

			x=x+1

	def update(self):
		self.blockSignals(True)
		for y in range(0,self.rowCount()):
			self.update_row(y)
		self.blockSignals(False)

	def callback_value_changed(self):
		root_path=self.refind_json_path()
		updated_token=""
		if root_path==None:
			return
		segments=self.bin.get_token_value(root_path,"segments")

		for segment in range(0,segments):
			x=0
			for t in self.json_tokens:
				token_path=root_path+".segment"+str(segment)
				found=True
				for a in t.split("."):
					is_token=self.bin.is_token(token_path,a)
					if is_token==False:
						found=False
						break
					last_path=token_path
					last_token=a

					token_path=token_path+"."+a
					t_last=a

				token_value=self.bin.get_token_value(last_path,last_token)
				if found==True:
					orig_json_type=type(token_value)
					wt=type(self.cellWidget(segment, x))
					cell_value=self.get_value(segment,x)
					if cell_value!="self_updating":
						if wt==edit_with_units:
							last_token=self.cellWidget(segment, x).token
							self.bin.set_token_value(last_path,last_token,str(cell_value[0]))
							self.bin.set_token_value(last_path,last_token+"_u",str(cell_value[1]))
						else:
							if str(cell_value).lower()!=str(token_value).lower():
								updated_token=t_last
							self.bin.set_token_value(last_path,last_token,str(cell_value))
				x=x+1

		self.changed.emit(updated_token)

	def callback_value_changed_direct(self):
		self.changed.emit("all")

	def refind_json_path(self):
		ret=None
		if self.uid==None:
			ret=self.json_root_path
		else:
			ret=self.bin.find_path_by_uid(self.json_root_path,self.uid)

		if self.json_postfix!=None:
			return ret+"."+self.json_postfix

		return ret

	def populate(self):
		if self.json_search_path!=None:
			print("Don't use json_search_path")
			adass
		root_path=self.refind_json_path()
		#print(root_path)
		segments=self.bin.get_token_value(root_path,"segments")

		for segment in range(0,segments):
			self.insert_row(root_path+".segment"+str(segment),segment)

	def remove_all_rows(self):
		self.blockSignals(True)
		self.setRowCount(0)
		self.blockSignals(False)

	def callback_menu_copy(self):
		if self.rowCount()==0:
			return
		root_path=self.refind_json_path()

		rows=self.selectionModel().selectedRows()
		row_numbers=[]
		for a in rows:
			row_number=a.row()
			row_numbers.append(row_number)

		self.bin.clipboard_copy(root_path,"",row_numbers)

	def callback_menu_paste(self):
		self.blockSignals(True)

		root_path=self.refind_json_path()
		row=self.get_new_row_pos()
		cb = QApplication.clipboard()
		text=cb.text()
		ret=self.bin.paste_append_segments_from_clipboard(root_path,"", row, text)

		for n in range(row,ret+row):
			self.insert_row(root_path+".segment"+str(n),n)

		self.blockSignals(False)
		self.changed.emit("all")

	def contextMenuEvent(self, event):
		if self.menu_disabled==False:
			self.menu.popup(QCursor.pos())

	def set_value(self,y,x,value,uid):

		self.setUpdatesEnabled(False)

		if self.cellWidget(y, x)!=None:
			self.cellWidget(y, x).blockSignals(True)
			if type(self.cellWidget(y, x))==QComboBox:
				self.cellWidget(y, x).setCurrentIndex(self.cellWidget(y, x).findText(value))
			elif type(self.cellWidget(y, x))==QComboBoxFiles:
				self.cellWidget(y, x).setValue(value)
			elif type(self.cellWidget(y, x))==QComboBoxLang:
				self.cellWidget(y, x).setValue_using_english(value)
			elif type(self.cellWidget(y,x))==g_select:
				self.cellWidget(y, x).setText(value)
			elif type(self.cellWidget(y,x))==energy_to_charge:
				self.cellWidget(y, x).updateValue(uid)
			elif type(self.cellWidget(y,x))==QLineEdit:
				self.cellWidget(y, x).setText(value)
			elif type(self.cellWidget(y,x))==g_applied_voltage:
				self.cellWidget(y, x).updateValue(uid)
			elif type(self.cellWidget(y,x))==g_majority_contact:
				self.cellWidget(y, x).updateValue(uid)
			elif type(self.cellWidget(y,x))==g_minority_contact:
				self.cellWidget(y, x).updateValue(uid)
			elif type(self.cellWidget(y,x))==g_probe_type:
				self.cellWidget(y, x).updateValue(uid)
			elif type(self.cellWidget(y,x))==gtkswitch:
				self.cellWidget(y, x).set_value(str2bool(value))
			elif type(self.cellWidget(y,x))==tab_button:
				pass
			else:
				self.cellWidget(y, x).set_value(value)
			self.cellWidget(y, x).blockSignals(False)
		else:
			item = self.item(y, x)
			if type(item)==QTableWidgetItem:
				item.setText(str(value))

		self.setUpdatesEnabled(True)

	def set_col_hidden(self,name,val):
		if name in self.json_tokens:
			i=self.json_tokens.index(name)
			if i>=0:
				self.setColumnHidden(i,val)

	def set_col_width(self,name,val):
		if name in self.json_tokens:
			i=self.json_tokens.index(name)
			if i>=0:
				self.setColumnWidth(i,val)

	def get_col_by_token(self,name):
		if name in self.json_tokens:
			i=self.json_tokens.index(name)
			return i
		return -1

	def get_value(self,y,x):
		if self.cellWidget(y, x)!=None and type(self.cellWidget(y, x))!=QWidget:
			if type(self.cellWidget(y, x))==QComboBox:
				return self.cellWidget(y, x).currentText()
			if type(self.cellWidget(y, x))==QComboBoxFiles:
				return self.cellWidget(y, x).currentText()
			elif type(self.cellWidget(y, x))==QComboBoxLang:
				return self.cellWidget(y, x).currentText_english()
			elif type(self.cellWidget(y,x))==g_select:
				return self.cellWidget(y, x).text()
			elif type(self.cellWidget(y,x))==energy_to_charge:
				return "self_updating"
			elif type(self.cellWidget(y,x))==QLineEdit:
				return self.cellWidget(y, x).text()
			elif type(self.cellWidget(y,x))==g_applied_voltage:
				return "self_updating"
			elif type(self.cellWidget(y,x))==g_majority_contact:
				return "self_updating"
			elif type(self.cellWidget(y,x))==g_minority_contact:
				return "self_updating"
			elif type(self.cellWidget(y,x))==g_probe_type:
				return self.cellWidget(y, x).text()
			elif type(self.cellWidget(y,x))==tab_button:
				pass
			else:
				return self.cellWidget(y, x).get_value()
		else:
			item = self.item(y, x)
			if type(item)==QTableWidgetItem:
				return item.text()

		return None

	def get_new_row_pos(self):
		index = self.selectionModel().selectedRows()

		if len(index)>0:
			pos=index[0].row()+1
		else:
			pos = self.rowCount()

		return pos

	def row_move_up_down(self,direction):
		ret=-1
		if self.rowCount()==0:
			return ret

		a=self.selectionModel().selectedRows()

		if len(a)==1:
			row=a[0].row()
			if row!=None:
				path=self.refind_json_path()
				self.blockSignals(True)
				#print(path,direction,row)
				a,b=self.bin.segments_move_up_down(path,direction,row)
				if a==None or b==None:
					return

				self.selectRow(b)
				self.update_row(a)
				self.update_row(b)
				self.blockSignals(False)
				self.changed.emit("all")

	def callback_move_up(self):
		self.row_move_up_down("up")

	def callback_move_down(self):
		self.row_move_up_down("down")

	def get_selected(self):
		a=self.selectionModel().selectedRows()

		if len(a)<=0:
			return False

		ret=[]
		
		for ii in range(0,len(a)):
			y=a[ii].row()
			for i in range(0,self.columnCount()):
				ret.append(str(self.get_value(y,i)))

		return ret

	def callback_remove_rows(self):
		self.blockSignals(True)
		path=self.refind_json_path()
		rows = []
		for index in self.selectedIndexes():
			row=index.row()
			if row not in rows:
				rows.append(row) 

		for row in sorted(rows, reverse=True):
			self.removeRow(row)
			self.bin.delete_segment(path,"segment"+str(row))
			self.selectRow(row)

		self.blockSignals(False)
		self.changed.emit("all")

	def set_row_color(self, rowIndex, color):
		self.blockSignals(True)
		for j in range(self.columnCount()):
			item=self.item(rowIndex, j)
			if item!=None:
				item.setBackground(color)
		self.blockSignals(False)

	def sync_selection(self, target_table):
		selected_indexes = self.selectionModel().selectedRows()
		if selected_indexes:
			row = selected_indexes[0].row()  # Get the selected row index
			target_table.selectRow(row)  # Select the same row in the target table
		else:
			target_table.clearSelection()
