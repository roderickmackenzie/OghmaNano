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

## @package select_param
#  Window to select a parameter to scan.
#


import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QTreeWidget, QPushButton, QHBoxLayout, QTreeWidgetItem
from PySide2.QtGui import QPainter,QIcon
from PySide2.QtGui import QFont

from icon_lib import icon_get
from error_dlg import error_dlg
from token_lib import tokens
from window_json_tree_view import window_json_tree_view
from sim_name import sim_name
class select_param(QWidget):

	def set_save_function(self,save_function):
		self.save_function=save_function

	def __init__(self,treeview):
		QWidget.__init__(self)
		self.my_token_lib=tokens()
		self.dest_treeview=treeview
		self.setMinimumSize(700,700)
		self.human_path_col=0
		self.json_path_col=-1
		self.main_vbox=QVBoxLayout()
		self.save_function=None

		self.setWindowIcon(icon_get("scan"))

		self.setWindowTitle(_("Select simulation parameter")+sim_name.web_window_title) 

		self.tab=window_json_tree_view()
		self.tab.english=True
		self.tab.show_values=False
		self.tab.update()
		
		self.main_vbox.addWidget(self.tab)

		self.hwidget=QWidget()

		okButton = QPushButton(_("OK"))
		cancelButton = QPushButton(_("Cancel"))

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(okButton)
		hbox.addWidget(cancelButton)

		self.hwidget.setLayout(hbox)

		self.main_vbox.addWidget(self.hwidget)

		self.setLayout(self.main_vbox)

		okButton.clicked.connect(self.tree_apply_click) 
		cancelButton.clicked.connect(self.close)


	def on_destroy(self):
		self.hide()
		return True

	
	def tree_apply_click(self):
		if self.dest_treeview==None:
			return
		
		index = self.dest_treeview.selectionModel().selectedRows()
		if len(index)>0:
			pos=index[0].row()
			node = self.tab.tab.selectedItems()
			json_path=self.tab.get_json_path(node)
			human_path=self.tab.get_human_path(node)
			self.dest_treeview.set_value(pos,self.human_path_col,human_path,None)
			#print(path)
			if self.json_path_col!=-1:
				self.dest_treeview.set_value(pos,self.json_path_col,json_path,None)

			if self.save_function!=None:
				self.save_function()

			self.close()
		else:
			error_dlg(self,_("No row selected in the scan window, can't insert the selection"))





