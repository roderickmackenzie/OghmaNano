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

## @package register
#  Registration window
#


import sys

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QApplication,QLineEdit,QComboBox,QHBoxLayout,QPushButton,QLabel,QDialog,QVBoxLayout,QSizePolicy
from PySide2.QtGui import QPainter,QIcon,QImage, QFont

from icon_lib import icon_get

from error_dlg import error_dlg
from gui_util import yes_no_dlg
from lock import lock
from spinner import spinner

def isValidEmail(email):
	if len(email) > 7:
		if email.count("@")==1:
			return True
	return False

from lock import get_lock
from cal_path import sim_paths
from json_base import json_base
from i18n import get_full_language
from sim_name import sim_name
import random

class register(QDialog):

	def callback_register(self):

		if self.anoym==False:
			if isValidEmail(self.email0.text()) == False :
				error_dlg(self,_("This is not a valide e-mail address"))
				return

			if self.email0.text()!=self.email1.text():
				error_dlg(self,_("The e-mail addresses do not match."))
				return

			if self.first_name.text()=="":
				error_dlg(self,_("Please enter your first name."))
				return

			if self.surname.text()=="":
				error_dlg(self,_("Please enter your surname."))
				return


			if self.company.text()=="":
				error_dlg(self,_("Please enter your Company/University."))
				return

		if self.heard_about.currentText()=="Choose option":
			error_dlg(self,_("Please enter how you heard about OghmaNano."))
			return

		if self.use_for.currentText()=="Choose option":
			error_dlg(self,_("Please enter what you plan on using OghmaNano for."))
			return

		#QApplication.processEvents()
		#QApplication.processEvents()

		#self.spinner.show()
		#self.working.show()
		if self.anoym==False:
			email=str(self.email0.text().encode('ascii', 'xmlcharrefreplace'))[2:-1]
			title=self.title.currentText()
			first_name=str(self.first_name.text().encode('ascii', 'xmlcharrefreplace'))[2:-1]
			surname=str(self.surname.text().encode('ascii', 'xmlcharrefreplace'))[2:-1]
			company=str(self.company.text().encode('ascii', 'xmlcharrefreplace'))[2:-1]
		else:
			email="abc@abc.com"
			title="Dr."
			first_name="none"
			surname="none"
			company="none"

		use_for=self.use_for.currentText()+":"+self.heard_about.currentText()
		use_for=str(use_for.encode('ascii', 'xmlcharrefreplace'))[2:-1]

		self.register.setEnabled(False)
		user_data=json_base("register")
		user_data.include_name=False
		user_data.var_list=[]
		user_data.var_list.append(["email",email])
		user_data.var_list.append(["title",title])
		user_data.var_list.append(["first_name",first_name])
		user_data.var_list.append(["surname",surname])
		user_data.var_list.append(["company",company])
		user_data.var_list.append(["use_for",use_for])
		user_data.var_list.append(["lang",get_full_language()])
		user_data.var_list_build()

		ret=get_lock().register(user_data)
		if ret==False:
			if get_lock().error=="no_internet":
				error_dlg(self,"I can't access the internet, or OghmaNano is down.")
			
			if get_lock().error=="too_old":
				error_dlg(self,_("Your version of OghmaNano is too old to register, please download the latest version."))

			return

		self.allow_exit=True

		self.accept()

	def __init__(self):
		QDialog.__init__(self)
		self.allow_exit=False
		self.setWindowIcon(icon_get("icon"))
		self.setWindowTitle(_("Registration window"+sim_name.web_window_title)) 
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		vbox=QVBoxLayout()

		l=QLabel(_("Please register to use OghmaNano. Thanks!"))
		l.setFont(QFont('SansSerif', 25))
		vbox.addWidget(l)

		hbox_widget=QWidget()
		hbox=QHBoxLayout()
		hbox_widget.setLayout(hbox)
		self.anoym=True

		if self.anoym==False:
			self.title = QComboBox()
			self.title.addItem("Dr.")
			self.title.addItem("Prof.")
			self.title.addItem("Mr.")
			self.title.addItem("Mrs.")
			self.title.addItem("Ms.")
			self.title.addItem("Other")
			hbox.addWidget(self.title)

			l=QLabel("<b>"+_("First name")+"</b>:")
			l.setFont(QFont('SansSerif', 14))
			hbox.addWidget(l)
			self.first_name = QLineEdit()

			hbox.addWidget(self.first_name)

			l=QLabel("<b>"+_("Surname")+"</b>:")
			l.setFont(QFont('SansSerif', 14))
			hbox.addWidget(l)
			self.surname = QLineEdit()
			hbox.addWidget(self.surname)
			vbox.addWidget(hbox_widget)
		

		#Company
		if self.anoym==False:
			hbox_widget=QWidget()
			hbox=QHBoxLayout()
			hbox_widget.setLayout(hbox)
			l=QLabel("<b>"+_("Company/University")+"</b>:")
			l.setFont(QFont('SansSerif', 14))
			hbox.addWidget(l)
			self.company = QLineEdit()
			hbox.addWidget(self.company)
			vbox.addWidget(hbox_widget)

		#Email 1
		if self.anoym==False:
			hbox_widget=QWidget()
			hbox=QHBoxLayout()
			hbox_widget.setLayout(hbox)
			l=QLabel("<b>"+_("E-mail")+"</b>:")
			l.setFont(QFont('SansSerif', 14))
			hbox.addWidget(l)
			self.email0 = QLineEdit()
			hbox.addWidget(self.email0)
			vbox.addWidget(hbox_widget)

		#Email 2
		if self.anoym==False:
			hbox_widget=QWidget()
			hbox=QHBoxLayout()
			hbox_widget.setLayout(hbox)
			l=QLabel("<b>"+_("Confirm e-mail")+"</b>:")
			l.setFont(QFont('SansSerif', 14))
			hbox.addWidget(l)
			self.email1 = QLineEdit()
			hbox.addWidget(self.email1)
			vbox.addWidget(hbox_widget)

		#Heard about
		hbox_widget=QWidget()
		hbox=QHBoxLayout()
		hbox_widget.setLayout(hbox)
		l=QLabel("<b>"+_("I heard about OghmaNano from:")+"</b>")
		l.setFont(QFont('SansSerif', 14))
		hbox.addWidget(l)
		self.heard_about = QComboBox()
		items=[]
		items.append("An accademic paper")
		items.append("My advisor")
		items.append("Google")
		items.append("Research gate")
		items.append("A friend")
		items.append("In class from my teacher")
		items.append("YouTube")
		items.append("Twitter")
		items.insert(0,"Other")
		random.shuffle(items)
		items.insert(0,"Choose option")

		for i in items:
			self.heard_about.addItem(i)

		hbox.addWidget(self.heard_about)
		vbox.addWidget(hbox_widget)

		#Use for
		hbox_widget=QWidget()
		hbox=QHBoxLayout()
		hbox_widget.setLayout(hbox)
		l=QLabel("<b>"+_("I am most interested in simulating:")+"</b>")
		l.setFont(QFont('SansSerif', 14))
		hbox.addWidget(l)
		self.use_for = QComboBox()
		items=[]
		items.append("Organic PV ")
		items.append("Perovskite PV")
		items.append("Other 3rd gen PV")
		items.append("2rd gen PV")
		items.append("1st gen PV")
		items.append("OLEDs")
		items.append("Micro optics")
		items.append("Ray tracing")
		items.append("FDTD")
		items.append("Thermal effects")
		items.append("Other")
		random.shuffle(items)
		items.insert(0,"Choose option")
		for i in items:
			self.use_for.addItem(i)

		hbox.addWidget(self.use_for)
		vbox.addWidget(hbox_widget)

		button_box=QHBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)
		self.register=QPushButton("Register", self)
		self.register.clicked.connect(self.callback_register)
		button_box.addWidget(self.register)

		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		vbox.addWidget(button_box_widget)

		self.setLayout(vbox)

		self.setMinimumWidth(400)

		if sim_paths.am_i_rod()==True:
			self.first_name.setText("Rod")
			self.surname.setText("Rod")
			self.email0.setText("r.c.i.mackenzie@googlemail.com")
			self.email1.setText("r.c.i.mackenzie@googlemail.com")
			self.company.setText("my company")
			self.use_for.setCurrentIndex(1)


	def closeEvent(self, event):
		if self.allow_exit==False:
			response=yes_no_dlg(self,sim_name.name.capitalize()+_(" will not work until you register.  Would do you want to exit?"))

			if response == True:
				sys.exit(0)

			event.ignore()
		else:
			event.accept()
		
	def run(self):
		return self.exec_()


