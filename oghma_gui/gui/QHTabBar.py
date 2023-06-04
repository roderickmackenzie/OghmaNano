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

## @package QHTabBar
#  A horizontal toolbar tab because QT does not have one.
#

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QMenu
from PySide2.QtGui import QIcon, QPainter, QFont, QColor,QMouseEvent
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox, QTabWidget,QStatusBar,QMenuBar, QTabBar, QStylePainter, QStyleOptionTab,QStyle
from gQtCore import gSignal
from icon_lib import icon_get
from json_root import json_root
import json
class QHTabBar(QTabBar):
	menu_click = gSignal(QMouseEvent,int)
	paste = gSignal()

	delete = gSignal()
	rename = gSignal()

	def menu_build(self):
		self.main_menu = QMenu(self)

		action=self.main_menu.addAction(icon_get("edit-copy"),_("Copy"))
		action.triggered.connect(self.do_copy)

		action=self.main_menu.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.do_paste)

		action=self.main_menu.addAction(icon_get("edit-delete"),_("Delete"))
		action.triggered.connect(self.do_delete)

		action=self.main_menu.addAction(icon_get("rename"),_("Rename"))
		action.triggered.connect(self.do_rename)
		#

	def do_delete(self):
		self.delete.emit()

	def do_rename(self):
		self.rename.emit()

	def do_copy(self):
		lines=None
		if self.obj_search_path!=None and self.obj_id!=None:
			search_path=eval(self.obj_search_path)
			obj=search_path.find_object_by_id(self.obj_id)
			lines=obj.gen_json()

		if lines!=None:
			lines[0]="\"data\": "+lines[0].split(":")[1]
			all_data=[]
			all_data.append("{")
			all_data.append("\"data_type\": \""+self.data_type+"\",")

			all_data.extend(lines)
			all_data.append("}")

			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText("\n".join(all_data), mode=cb.Clipboard)

	def do_paste(self):
		lines = QApplication.clipboard().text()
		#try:
		read_data=json.loads(lines)
		#except:
		#	return
		self.paste_data=read_data['data']
		self.paste.emit()

	def show_menu_tab(self,event,tab_number):
		self.main_menu.exec_(event.globalPos())

	def __init__(self,build_tb=False):
		QTabBar.__init__(self)

		if build_tb==True:
			self.box=QVBoxLayout()
			self.box.setSpacing(0)
			self.box.setContentsMargins(0, 0, 0, 0)
			self.setLayout(self.box)
			self.box_tb0=QToolBar()
			self.box_tb0.setIconSize(QSize(32, 32))
			self.box.addWidget(self.box_tb0)
			self.box_tb1=QToolBar()
			self.box_tb1.setIconSize(QSize(32, 32))
			self.box.addWidget(self.box_tb1)
			

			self.tb_copy = QAction(icon_get("edit-copy"), wrap_text(_("Copy"),3), self)
			self.box_tb0.addAction(self.tb_copy)

			self.tb_paste = QAction(icon_get("edit-paste"), wrap_text(_("Paste"),3), self)
			self.box_tb1.addAction(self.tb_paste)
			self.tb_copy.triggered.connect(self.do_copy)
			self.tb_paste.triggered.connect(self.do_paste)


		self.menu_build()

		self.data_type="none"
		self.paste_data=None

		self.obj_search_path=None
		self.obj_id=None


		self.setStyleSheet("QTabBar::tab { height: 35px; width: 140px; }")

	def paintEvent(self, event):
		painter = QStylePainter(self)
		option = QStyleOptionTab()

		#painter.begin(self)
		for index in range(self.count()):
			self.initStyleOption(option, index)
			tabRect = self.tabRect(index)
			tabRect.moveLeft(10)
			painter.drawControl(QStyle.CE_TabBarTabShape, option)
			painter.drawText(tabRect, Qt.AlignVCenter | Qt.TextDontClip, self.tabText(index))
		#painter.end()

	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			tab_index=self.tabAt(event.pos())
			#self.obj_id=tab.uid
			#self.menu_click.emit(event,self.tabAt(event.pos()))
			self.show_menu_tab(event,tab_index)
		QTabBar.mousePressEvent(self, event)


