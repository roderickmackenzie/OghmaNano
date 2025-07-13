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

## @package QComboBoxLang
#  A combobox which displays the native language but has an english back end.
#
import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox
from gQtCore import gSignal
from icon_lib import icon_get

class QComboBoxLang(QComboBox):
	
	class my_lang_obj():
		def __init__(self):
			self.english=""
			self.lang=""
			self.icon=None

	def __init__(self):
		QComboBox.__init__(self)
		self.setIconSize(QSize(32, 32))
		self.objs=[]

	def addItemLangIcon(self,english,lang,icon):
		obj=self.my_lang_obj()
		obj.english=english
		obj.lang=lang
		obj.icon=icon
		self.objs.append(obj)
		print(icon)
		icon_png=icon_get(icon)
		super().addItem(icon_png, lang)
		self.setItemIcon(self.count() - 1, icon_png)
		
	def addItemLang(self,english,lang):
		obj=self.my_lang_obj()
		obj.english=english
		obj.lang=lang
		self.objs.append(obj)
		self.addItem(lang)
	
	def setValue_using_english(self,english):
		pos=None
		for i in range(0,len(self.objs)):
			if self.objs[i].english==english:
				pos=i
				break

		if pos!=None:
			self.setCurrentIndex(pos)

	def currentText_english(self):
		for i in range(0,len(self.objs)):
			if self.objs[i].lang==self.currentText():
				pos=i
				break

		return self.objs[pos].english
	



