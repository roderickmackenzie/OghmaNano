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

## @package gui_util
#  GUI utilities.
#


#qt
from gui_enable import gui_get

if gui_get()==True:
	from PySide2.QtWidgets import QTextEdit, QAction,QTableWidgetItem,QComboBox, QMessageBox, QDialog, QDialogButtonBox
	from PySide2.QtWidgets import QListWidgetItem,QListView,QLineEdit,QWidget,QHBoxLayout,QPushButton, QSpinBox
	from PySide2.QtGui import QPixmap, QIcon
	from gQtCore import QSize, Qt, QTimer
	from QComboBoxLang import QComboBoxLang
	from gtkswitch import gtkswitch
	from icon_widget import icon_widget
	from leftright import leftright
	from g_select import g_select
	from QComboBoxLang import QComboBoxLang
	from QColorPicker import QColorPicker
	from QColorPicker import QColorPicker_one_line
	from QChangeLog import QChangeLog
	from generic_switch import generic_switch
	from g_select import g_select_electrical_edit
	from mobility_widget import mobility_widget
	from QComboBoxLayers import QComboBoxLayers
	from QComboBoxOpenCL import QComboBoxOpenCL
	from edit_with_units import edit_with_units
	from QComboBoxNetworkInputs import QComboBoxNetworkInputs
	from QComboBoxNetworkOutputs import QComboBoxNetworkOutputs
#windows
from icon_lib import icon_get
from str2bool import str2bool


def yes_no_dlg(parent,text):
	msgBox = QMessageBox(parent)
	msgBox.setIcon(QMessageBox.Question)
	msgBox.setText("Question")
	msgBox.setInformativeText(text)
	msgBox.setStandardButtons(QMessageBox.Yes| QMessageBox.No )
	msgBox.setDefaultButton(QMessageBox.No)
	reply = msgBox.exec_()
	if reply == QMessageBox.Yes:
		return True
	else:
		return False

def widget_get_value(widget):
	if type(widget)==QLineEdit:
		return widget.text()
	elif type(widget)==QSpinBox:
		return widget.value()
	elif type(widget)==g_select:
		return widget.text()
	elif type(widget)==icon_widget:
		return widget.text()
	elif type(widget)==QComboBox:
		return widget.itemText(widget.currentIndex())
	elif type(widget)==QComboBoxLang:
		return widget.currentText_english()
	elif type(widget)==QColorPicker_one_line:
		return str(widget.r)+","+str(widget.g)+","+str(widget.b)+","+str(widget.alpha)
	elif type(widget)==QChangeLog:
		return widget.toPlainText()
	elif type(widget)==QComboBoxLayers:
		return widget.currentText()
	elif type(widget)==QComboBoxOpenCL:
		return widget.currentText()
	elif type(widget)==mobility_widget:
		return widget.get_values()
	else:
		try:
			return widget.get_value()
		except:
			return None

def widget_set_value(widget,value,unit=""):

	widget.blockSignals(True)
	if type(widget)==QLineEdit:
		widget.setText(str(value))
	elif type(widget)==gtkswitch:
		widget.set_value(str2bool(value))
	elif type(widget)==QSpinBox:
		widget.setValue(int(value))
	elif type(widget)==leftright:
		widget.set_value(str2bool(value))
	elif type(widget)==g_select:
		widget.setText(value)
	elif type(widget)==icon_widget:
		widget.setText(value)
	elif type(widget)==QComboBox:
		all_items  = [widget.itemText(i) for i in range(widget.count())]
		for i in range(0,len(all_items)):
			if all_items[i] == value:
				widget.setCurrentIndex(i)
				break
	elif type(widget)==QComboBoxLang:
		widget.setValue_using_english(value)
	elif type(widget)==QColorPicker:
		pass
	elif type(widget)==QColorPicker_one_line:
		widget.setText(value)
	elif type(widget)==QChangeLog:
		widget.setText(value)
	elif type(widget)==QComboBoxLayers:
		return widget.setValue(value)
	elif type(widget)==QComboBoxOpenCL:
		pass
	elif type(widget)==mobility_widget:
		widget.set_values(value)
	else:
		widget.set_value(value)

	widget.blockSignals(False)


