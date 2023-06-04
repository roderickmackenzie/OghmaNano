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

## @package energy_to_charge
#  A widget for the tab widget which allows the user to select files.
#



#qt
from PySide2.QtWidgets import QMainWindow,QLabel, QTextEdit, QTableWidgetItem,QComboBox, QMessageBox
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton
from gQtCore import QSize, Qt
from QComboBoxLang import QComboBoxLang

#cal_path
from gQtCore import gSignal

from epitaxy import get_epi
from dos_io import gen_fermi_from_np
from dos_io import gen_np_from_fermi
import decimal

from json_root import json_root

import i18n
_ = i18n.language.gettext


class energy_to_charge(QWidget):


	def __init__(self):
		QWidget.__init__(self)
		self.hbox=QHBoxLayout()
		self.edit_m3=QLineEdit()
		self.edit_m3.setMaximumWidth( 60 )
		self.label_m3=QLabel("m<sup>-3</sup> /")
		self.label_m3.setStyleSheet("QLabel { border: 0px; padding: 0px; }");
		self.label_m3.setMaximumWidth( 30 )

		self.edit_eV=QLineEdit()
		self.edit_eV.setMaximumWidth( 50 )
		self.label_eV=QLabel("eV")
		self.label_eV.setStyleSheet("QLabel { border: 0px; padding: 0px; }");
		self.label_eV.setMaximumWidth( 20 )

		self.hbox.addWidget(self.edit_m3,Qt.AlignLeft)
		self.hbox.addWidget(self.label_m3,Qt.AlignLeft)
		self.hbox.addWidget(self.edit_eV,Qt.AlignLeft)
		self.hbox.addWidget(self.label_eV,Qt.AlignLeft)
		self.hbox.setSpacing(0)

		self.edit_m3.textChanged.connect(self.callback_m3_changed)
		self.edit_eV.textChanged.connect(self.callback_eV_changed)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit_m3.setStyleSheet("QLineEdit { border: none }");

		self.setLayout(self.hbox)

	def cal_ev(self):
		self.find_layer_and_contact()
		if self.contact.charge_type=="electron":
			eV=gen_fermi_from_np(float(self.edit_m3.text()),self.layer.shape_dos.Nc,300.0)
		else:
			eV=gen_fermi_from_np(float(self.edit_m3.text()),self.layer.shape_dos.Nv,300.0)
		return eV

	def cal_m3(self):
		self.find_layer_and_contact()
		try:
			Ef=float(self.edit_eV.text())
		except:
			return False

		if self.contact.charge_type=="electron":
			n=gen_np_from_fermi(Ef,self.layer.shape_dos.Nc,300.0)
		else:
			n=gen_np_from_fermi(Ef,self.layer.shape_dos.Nv,300.0)
		return n


	

	def edit_m3_update(self,n):
		try:
			val=float(n)
		except:
			return
		text='%.2e' % val
		text=str(decimal.Decimal(text).normalize()).lower().replace('+', '')
		self.edit_m3.setText(text)

		#self.edit_m3.setText('%.0e' % n)

	def edit_eV_update(self,ev):
		try:
			val=float(ev)
		except:
			return

		self.edit_eV.setText('%.2f' % val)

	def callback_eV_changed(self):
		n=self.cal_m3()
		if n==False:
			return
		self.edit_m3.blockSignals(True)
		self.edit_m3_update(n)
		self.edit_m3.blockSignals(False)
		self.contact.np=float(n)
		json_root().save()

	def callback_m3_changed(self):
		try:
			ev=self.cal_ev()
			self.edit_eV.blockSignals(True)
			self.edit_eV_update(ev)
			self.edit_eV.blockSignals(False)
			self.contact.np=float(self.edit_m3.text())
		except:
			pass
		json_root().save()

	def find_layer_and_contact(self):
		self.layer=None
		self.contact=None
		for c in get_epi().contacts.segments:
			if self.uid==c.id:
				if c.position=="top":
					for l in get_epi().layers:
						if l.layer_type=="active":
							self.layer=l
							self.contact=c
							break
				elif c.position=="bottom":
					n=len(get_epi().layers)-1
					while(n>=0):
						l=get_epi().layers[n]
						if l.layer_type=="active":
							self.layer=l
							self.contact=c
							break
						n=n-1

	def updateValue(self,uid):
		self.uid=uid
		self.update()

	def update(self):
		self.find_layer_and_contact()
		if self.contact==None:
			return
		self.edit_m3.blockSignals(True)
		self.edit_m3_update(self.contact.np)
		self.edit_m3.blockSignals(False)
		ev=self.cal_ev()
		self.edit_eV.blockSignals(True)
		self.edit_eV_update(ev)
		self.edit_eV.blockSignals(False)

	def text(self):
		return self.contact.np
		
