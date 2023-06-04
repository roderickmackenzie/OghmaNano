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

## @package optics_ribbon
#  The ribbon for the optics window
#


import os

from cal_path import get_css_path

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit, QToolButton, QMenu
from PySide2.QtWidgets import QTabWidget

from icon_lib import icon_get

from about import about_dlg

from util import wrap_text
from ribbon_base import ribbon_base
from play import play
from QAction_lock import QAction_lock
from generation_rate_editor import generation_rate_editor
from json_root import json_root
from help import QAction_help

class mode_button(QAction_lock):
	def __init__(self,image,text,s,name):
		QAction_lock.__init__(self,image,text,s,name)
		self.setCheckable(True)
		self.mode="full"


class ribbon_optics_files(QToolBar):
	def __init__(self):
		QToolBar.__init__(self)

		self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.setIconSize(QSize(42, 42))
		
		self.run = play(self,"optics_ribbon_run",run_text=wrap_text(_("Run optical simulation"),5))
		self.addAction(self.run)


		self.configwindow = QAction(icon_get("preferences-system"), _("Configure"), self)
		self.addAction(self.configwindow)

		self.build_action_group()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)

		self.optical_thickness = QAction(icon_get("optical_thickness"), _("Optical\nthickness"), self)
		self.addAction(self.optical_thickness)

		self.help = QAction_help()
		self.addAction(self.help)

	def build_action_group(self):
		self.actions=[]
		self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.setIconSize(QSize(42, 42))
		
		a=mode_button("transfer_matrix", _("Transfer\nmatrix"), self,"optics_ribbon_export_image")
		a.mode="full"
		a.clicked.connect(self.callback_click)
		self.actions.append(a)

		a=mode_button("exp_light", _("Exponential\nprofile"), self,"optics_ribbon_mode_exp")
		a.mode="exp"
		a.clicked.connect(self.callback_click)
		self.actions.append(a)

		a=mode_button("flat_light", _("Flat\nprofile"), self,"optics_ribbon_mode_flat")
		a.mode="flat"
		a.clicked.connect(self.callback_click)
		self.actions.append(a)

		a=mode_button("file_light", _("From\nfile"), self,"optics_ribbon_mode_from_file")
		a.mode="fromfile"
		a.clicked.connect(self.callback_click)
		self.actions.append(a)

		a=mode_button("qe_light", _("From QE\nspectra"), self,"optics_ribbon_mode_qe")
		a.mode="qe"
		a.clicked.connect(self.callback_click)
		self.actions.append(a)

		a=mode_button("constant_light", _("Constant\nvalue"), self,"optics_ribbon_mode_constant")
		a.mode="constant"
		a.clicked.connect(self.callback_click)

		self.menu_set_constant_value = QMenu(self)
		#self.populate_used_file_menu()
		a.setMenu(self.menu_set_constant_value)

		f=QAction(_("Edit constant"), self)
		f.triggered.connect(self.callback_edit_constant)
		self.menu_set_constant_value.addAction(f)


		self.actions.append(a)

		for a in self.actions:
			self.addAction(a)

		self.set_mode()

	def callback_edit_constant(self):
		self.generation_rate_editor=generation_rate_editor()
		self.generation_rate_editor.show()

	def set_mode(self):
		self.blockSignals(True)
		data=json_root()
		used_model=data.optical.light.light_model
		for a in self.actions:
			a.setChecked(False)
			if a.mode==used_model:
				a.setChecked(True)
				break

		self.blockSignals(False)

	def callback_click(self,w):
		self.blockSignals(True)
		data=json_root()

		for a in self.actions:
			a.setChecked(False)

		w.setChecked(True)

		data.optical.light.light_model=w.mode
		data.save()

		self.blockSignals(False)

class optics_ribbon(ribbon_base):

	def update(self):
		return

	def callback_about_dialog(self):
		dlg=about_dlg()
		dlg.exec_()

	def __init__(self):
		QTabWidget.__init__(self)
		#self.setStyleSheet("QWidget {	background-color:cyan; }")

		self.about = QToolButton(self)
		self.about.setText(_("About"))
		self.about.pressed.connect(self.callback_about_dialog)

		self.setCornerWidget(self.about)

		self.optics=ribbon_optics_files()
		self.addTab(self.optics,_("Optics"))

		sheet=self.readStyleSheet(os.path.join(get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

		self.update()
