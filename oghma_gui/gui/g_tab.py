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

## @package g_tab
#  A table widget
#


#qt
from PySide2.QtWidgets import QTextEdit, QAction, QMenu
from gQtCore import QSize, Qt , QPersistentModelIndex
from PySide2.QtWidgets import QWidget,QPushButton,QToolBar, QVBoxLayout, QTableWidget,QAbstractItemView, QTableWidgetItem, QComboBox, QApplication
from PySide2.QtGui import QCursor
from gQtCore import gSignal

from QComboBoxLang import QComboBoxLang
from icon_lib import icon_get

from g_select import g_select
from energy_to_charge import energy_to_charge

from gtkswitch import gtkswitch
from leftright import leftright
from str2bool import str2bool

class g_tab(QTableWidget):

	changed = gSignal()
	user_remove_rows = gSignal()

	def __init__(self,toolbar=None):
		QTableWidget.__init__(self)
		self.toolbar=toolbar
		self.setSelectionBehavior(QAbstractItemView.SelectItems)
		self.SelectionMode (QAbstractItemView.SingleSelection)
		
		if self.toolbar!=None:
			self.toolbar.setIconSize(QSize(32, 32))
			self.tb_add = QAction(icon_get("list-add"), _("Add"), self)
			self.toolbar.addAction(self.tb_add)

			self.tb_remove = QAction(icon_get("list-remove"), _("Delete row"), self)
			self.toolbar.addAction(self.tb_remove)
			self.tb_remove.triggered.connect(self.emit_remove_rows)

			self.tb_down= QAction(icon_get("go-down"), _("Move down"), self)
			self.toolbar.addAction(self.tb_down)

			self.tb_up= QAction(icon_get("go-up"), _("Move up"), self)
			self.toolbar.addAction(self.tb_up)

		self.menu = QMenu(self)

		self.menu_delete = QAction(icon_get("list-remove"),_("Delete row"), self)
		self.menu.addAction(self.menu_delete)
		self.menu_delete.triggered.connect(self.emit_remove_rows)


	def contextMenuEvent(self, event):
		self.menu.popup(QCursor.pos())

	def set_value(self,y,x,value):
		if type(self.cellWidget(y, x))==QComboBox:
			self.cellWidget(y, x).blockSignals(True)
			self.cellWidget(y, x).setCurrentIndex(self.cellWidget(y, x).findText(value))
			self.cellWidget(y, x).blockSignals(False)
		elif type(self.cellWidget(y, x))==QComboBoxLang:
			self.cellWidget(y, x).blockSignals(True)
			self.cellWidget(y, x).setValue_using_english(value)
			self.cellWidget(y, x).blockSignals(False)
		elif type(self.cellWidget(y,x))==g_select:
			self.cellWidget(y, x).blockSignals(True)
			self.cellWidget(y, x).setText(value)
			self.cellWidget(y, x).blockSignals(False)
		elif type(self.cellWidget(y,x))==energy_to_charge:
			self.cellWidget(y, x).blockSignals(True)
			self.cellWidget(y, x).updateValue(value)
			self.cellWidget(y, x).blockSignals(False)
		elif type(self.cellWidget(y,x))==gtkswitch:
			self.cellWidget(y, x).blockSignals(True)
			self.cellWidget(y, x).set_value(str2bool(value))
			self.cellWidget(y, x).blockSignals(False)
		else:
			item = QTableWidgetItem(str(value))
			self.setItem(y,x,item)

	def move_down(self):
		ret=-1

		if self.rowCount()==0:
			return -1

		self.blockSignals(True)
		a=self.selectionModel().selectedRows()

		if len(a)>0:
			a=a[0].row()

			b=a+1
			if b>self.rowCount()-1:
				return -1

			ret=a

			av=[]
			for i in range(0,self.columnCount()):
				av.append(str(self.get_value(a,i)))

			bv=[]
			for i in range(0,self.columnCount()):
				bv.append(str(self.get_value(b,i)))

			for i in range(0,self.columnCount()):
				self.set_value(b,i,str(av[i]))
				self.set_value(a,i,str(bv[i]))

			self.selectRow(b)
			self.blockSignals(False)
			return ret
		else:
			return -1

	def get_value(self,y,x):
		if type(self.cellWidget(y, x))==QComboBox:
			return self.cellWidget(y, x).currentText()
		elif type(self.cellWidget(y, x))==QComboBoxLang:
			return self.cellWidget(y, x).currentText_english()
		elif type(self.cellWidget(y,x))==g_select:
			return self.cellWidget(y, x).text()
		elif type(self.cellWidget(y,x))==energy_to_charge:
			return self.cellWidget(y, x).text()
		elif type(self.cellWidget(y,x))==leftright:
			return self.cellWidget(y, x).get_value()
		elif type(self.cellWidget(y,x))==gtkswitch:
			return self.cellWidget(y, x).get_value()
		else:
			return self.item(y, x).text()


	def add(self,data):
		self.blockSignals(True)
		index = self.selectionModel().selectedRows()

		if len(index)>0:
			pos=index[0].row()+1
		else:
			pos = self.rowCount()

		if self.columnCount()==len(data):
			self.insertRow(pos)
			for i in range(0,len(data)):
				self.setItem(pos,i,QTableWidgetItem(data[i]))

		if len(data)>self.columnCount():
			rows=int(len(data)/self.columnCount())
			for ii in range(0,rows):
				self.insertRow(pos)
				for i in range(0,self.columnCount()):
					self.setItem(pos,i,QTableWidgetItem(data[ii*tab.columnCount()+i]))
				pos=pos+1
					
		self.blockSignals(False)

	def insert_row(self):
		self.blockSignals(True)
		index = self.selectionModel().selectedRows()

		if len(index)>0:
			pos=index[0].row()+1
		else:
			pos = self.rowCount()

		self.insertRow(pos)
		self.blockSignals(False)
		return pos

	def move_up(self):
		ret=-1
		if self.rowCount()==0:
			return ret

		self.blockSignals(True)
		a=self.selectionModel().selectedRows()

		if len(a)==1:
			a=a[0].row()	

			b=a-1
			if b<0:
				return -1
				#b=tab.rowCount()-1

			ret=a

			av=[]
			for i in range(0,self.columnCount()):
				av.append(str(self.get_value(a,i)))

			bv=[]
			for i in range(0,self.columnCount()):
				bv.append(str(self.get_value(b,i)))

			for i in range(0,self.columnCount()):
				self.set_value(b,i,str(av[i]))
				self.set_value(a,i,str(bv[i]))

			self.selectRow(b)
			self.blockSignals(False)
			return ret

		else:
			return ret

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

	def emit_remove_rows(self):
		self.user_remove_rows.emit()

	def remove(self):
		self.blockSignals(True)

		rows = []
		for index in self.selectedIndexes():
			row=index.row()
			if row not in rows:
				rows.append(row) 

		for row in sorted(rows, reverse=True):
			self.removeRow(row)

		self.blockSignals(False)

		self.changed.emit()

