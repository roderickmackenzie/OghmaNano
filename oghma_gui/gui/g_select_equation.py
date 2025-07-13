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

## @package g_select_from_db
#  A widget for the tab widget which allows the user to select material files.
#



from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton
from gQtCore import gSignal
from cal_path import subtract_paths
from g_select_base import g_select_base
from cal_path import sim_paths
from inode import inode
from bytes2str import str2bytes

import i18n
_ = i18n.language.gettext


class g_select_equation(g_select_base):

	changed = gSignal()

	def __init__(self,file_box=True):
		self.is_lumo=True
		g_select_base.__init__(self)

		self.button.clicked.connect(self.callback_button_click)
		self.edit.textChanged.connect(self.text_changed)

	def text_changed(self):
		self.changed.emit()

	def callback_button_click(self):
		from g_open import g_open

		items=[]
		itm=inode()
		itm.file_name=b"gaussian"
		itm.icon=b"gaussian"
		itm.type=b"file"
		itm.display_name=str2bytes(_("Gaussian"))
		itm.can_delete=False
		items.append(itm)

		itm=inode()
		itm.file_name=b"lorentzian"
		itm.icon=b"lorentzian"
		itm.type=b"file"
		itm.display_name=str2bytes(_("Lorentzian"))
		itm.can_delete=False
		items.append(itm)

		itm=inode()
		itm.file_name=b"power_law_deibel"
		itm.icon=b"power_law"
		itm.type=b"file"
		itm.display_name=str2bytes(_("Power law"))
		itm.can_delete=False
		items.append(itm)


		itm=inode()
		itm.file_name=b"exponential"
		itm.icon=b"exponential"
		itm.type=b"file"
		itm.display_name=str2bytes(_("Exponential"))
		itm.can_delete=False
		items.append(itm)

		dialog=g_open("/equations/",act_as_browser=False,fake_dir_structure=items)
		
		ret=dialog.exec_()
		if ret==QDialog.Accepted:
			file_name=dialog.get_filename()
			equation=file_name.split("/")[2]
			val=""
			if equation=="gaussian":
				if self.is_lumo==True:
					val="a*exp(-((c+(E-Ec))/(sqrt(2.0)*b*1.0))^2.0)"
				else:
					val="a*exp(-((c+(Ev-E))/(sqrt(2.0)*b*1.0))^2.0)"
			elif equation=="lorentzian":
				if self.is_lumo==True:
					val="((3.14*b)/2.0)*a*(1.0/3.1415926)*(0.5*b/((E-Ec+c)*(E-Ec+c)+(0.5*b)*(0.5*b)))"
				else:
					val="((3.14*b)/2.0)*a*(1.0/3.1415926)*(0.5*b/((Ev-E+c)*(Ev-E+c)+(0.5*b)*(0.5*b)))"
			elif equation=="power_law_deibel":
				if self.is_lumo==True:
					val="a*exp((E-Ec)/(b+(E-Ec)/c))"
				else:
					val="a*exp((Ev-E)/(b+(Ev-E)/c))"
			elif equation=="exponential":
				if self.is_lumo==True:
					val="a*exp((E-Ec)/b)"
				else:
					val="a*exp((Ev-E)/b)"
			else:
				val="a"

			self.set_value(val)
			self.changed.emit()
		



