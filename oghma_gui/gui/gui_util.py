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


from cal_path import get_image_file_path

#qt
from gui_enable import gui_get

if gui_get()==True:
	from PySide2.QtWidgets import QTextEdit, QAction,QTableWidgetItem,QComboBox, QMessageBox, QDialog, QDialogButtonBox
	from PySide2.QtWidgets import QListWidgetItem,QListView,QLineEdit,QWidget,QHBoxLayout,QPushButton
	from PySide2.QtGui import QPixmap, QIcon
	from gQtCore import QSize, Qt, QTimer
	from QComboBoxLang import QComboBoxLang
	from gtkswitch import gtkswitch
	from g_select_material import g_select_material
	from g_select_filter import g_select_filter
	from g_select_shape import g_select_shape
	from icon_widget import icon_widget
	from leftright import leftright
	from g_select import g_select
	from QComboBoxLang import QComboBoxLang
	from QColorPicker import QColorPicker
	from QColorPicker import QColorPicker_one_line
	from QComboBoxNewtonSelect import QComboBoxNewtonSelect
	from QChangeLog import QChangeLog
	from generic_switch import generic_switch
	from shape_dos_switch import shape_dos_switch
	from shape_electrical_switch import shape_electrical_switch
	from mobility_widget import mobility_widget
	from QComboBoxLayers import QComboBoxLayers
	from QComboBoxOpenCL import QComboBoxOpenCL

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
	elif type(widget)==gtkswitch:
		return widget.get_value()
	elif type(widget)==leftright:
		return widget.get_value()
	elif type(widget)==g_select:
		return widget.text()
	elif type(widget)==g_select_material:
		return widget.text()
	elif type(widget)==g_select_filter:
		return widget.text()
	elif type(widget)==g_select_shape:
		return widget.text()
	elif type(widget)==icon_widget:
		return widget.text()
	elif type(widget)==QComboBox:
		return widget.itemText(widget.currentIndex())
	elif type(widget)==QComboBoxLang:
		return widget.currentText_english()
	elif type(widget)==QColorPicker:
		return widget.get_value()
	elif type(widget)==QColorPicker_one_line:
		return str(widget.r)+","+str(widget.g)+","+str(widget.b)+","+str(widget.alpha)
	elif type(widget)==QChangeLog:
		return widget.toPlainText()
	elif type(widget)==QComboBoxNewtonSelect:
		return widget.currentText()
	elif type(widget)==QComboBoxLayers:
		return widget.currentText()
	elif type(widget)==QComboBoxOpenCL:
		return widget.currentText()
	elif type(widget)==generic_switch:
		return widget.get_value()
	elif type(widget)==shape_dos_switch:
		return widget.get_value()
	elif type(widget)==shape_electrical_switch:
		return widget.get_value()
	elif type(widget)==mobility_widget:
		return widget.get_values()
	else:
		return None

def widget_set_value(widget,value):

	widget.blockSignals(True)
	if type(widget)==QLineEdit:
		widget.setText(str(value))
	elif type(widget)==gtkswitch:
		widget.set_value(str2bool(value))
	elif type(widget)==leftright:
		widget.set_value(str2bool(value))
	elif type(widget)==g_select:
		widget.setText(value)
	elif type(widget)==g_select_material:
		widget.setText(value)
	elif type(widget)==g_select_filter:
		widget.setText(value)
	elif type(widget)==g_select_shape:
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
	elif type(widget)==QComboBoxNewtonSelect:
		widget.setValue(value)
	elif type(widget)==QComboBoxLayers:
		return widget.setValue(value)
	elif type(widget)==QComboBoxOpenCL:
		pass
	elif type(widget)==generic_switch:
		widget.set_value(value)
	elif type(widget)==shape_dos_switch:
		widget.set_value(value)
	elif type(widget)==shape_electrical_switch:
		widget.set_value(value)
	elif type(widget)==mobility_widget:
		widget.set_values(value)
	else:
		print("ooops")

	widget.blockSignals(False)


