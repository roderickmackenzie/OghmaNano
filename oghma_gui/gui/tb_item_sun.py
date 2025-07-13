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

## @package tb_item_sun
#  A toolbar item to select the sun's intensity.
#


#inp

import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox
from gQtCore import gSignal

from global_objects import global_object_run
from json_c import json_tree_c

class tb_item_sun(QWidget):

	changed = gSignal()
	def __init__(self,layout=QVBoxLayout()):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		label=QLabel()
		if type(layout)==QVBoxLayout:
			label.setText(_("Light intensity")+" ("+_("Suns")+"):")
		else:
			label.setText(_("Light intensity")+"\n("+_("Suns")+"):")

		layout.addWidget(label)

		self.light = QComboBox(self)
		self.light.setEditable(True)


		layout.addWidget(self.light)

		self.setLayout(layout)

		self.update()
		
		self.light.currentIndexChanged.connect(self.call_back_light_changed)
		self.light.editTextChanged.connect(self.call_back_light_changed)

	def call_back_light_changed(self):
		light_power=self.light.currentText()
		try:
			self.bin.set_token_value("optical.light_sources","Psun",float(light_power))
		except:
			pass
		self.bin.save()
		global_object_run("gl_force_redraw")
		self.changed.emit()

	def update(self):
		self.light.blockSignals(True)
		self.light.clear()
		sun_values=["0.0","0.01","0.1","1.0","10"]

		token=str(self.bin.get_token_value("optical.light_sources","Psun"))

		if sun_values.count(token)==0:
			sun_values.append(token)

		for i in range(0,len(sun_values)):
			self.light.addItem(sun_values[i])

		all_items  = [self.light.itemText(i) for i in range(self.light.count())]
		for i in range(0,len(all_items)):
		    if all_items[i] == token:
		        self.light.setCurrentIndex(i)
		self.light.blockSignals(False)



