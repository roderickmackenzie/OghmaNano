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

## @package help
#  Help window on the top right.
#


import os
from cal_path import get_icon_path
import webbrowser

from gQtCore import QSize, Qt
from PySide2.QtGui import QIcon,QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout,QProgressBar,QLabel,QDesktopWidget,QToolBar,QHBoxLayout,QAction,QSizePolicy,QStatusBar
from PySide2.QtGui import QPixmap

from i18n import get_language

from cal_path import get_flag_file_path
from i18n import get_full_desired_lang_path

from bibtex import bibtex
from icon_lib import icon_get
from sim_name import sim_name
my_help_class=None

class QAction_help(QAction):
	def __init__(self):
		QAction.__init__(self,icon_get("internet-web-browser"), _("Help"), None)
		self.setStatusTip(_("Help"))
		self.triggered.connect(self.callback_help)

	def callback_help(self):
		webbrowser.open(sim_name.web+"/docs.html")

class help_data():
	def __init__(self,token,icon,text):
		self.token=token
		self.icon=icon
		self.text=text

class help_class(QWidget):
	def move_window(self):
		shape=QDesktopWidget().screenGeometry()

		w=shape.width()
		shape.height()
		win_w=self.frameGeometry().width()
		self.frameGeometry().height()

		x=w-win_w
		y=50
		self.move(x,y)

	def help_show(self):
		self.show()
		self.move_window()

	def toggle_visible(self):
		if self.isVisible()==True:
			self.setVisible(False)
		else:
			self.setVisible(True)

		self.move_window()

	def __init__(self):
		QWidget.__init__(self)
		self.item_height=10
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
		#self.setFixedSize(400,160)
		#self.setFixedWidth(700)

		self.setStyleSheet(" padding:0px; margin-top:0px; margin-bottom:0px")
		#; border:2px solid rgb(0, 0, 0); 

		self.last=[]
		self.pos=-1

		self.move_window()
		self.vbox = QVBoxLayout()

		#self.vbox.setAlignment(Qt.AlignTop)
		self.box=[]
		self.image=[]
		self.label=[]
		for i in range(0,5):
			l=QHBoxLayout()
			label=QLabel()
			label.setWordWrap(True)
			label.setOpenExternalLinks(True)
			image=QLabel()
			font = QFont()
			font.setPointSize(18)
			label.setFont(font)

			image.setFixedWidth(64)
			image.setAlignment(Qt.AlignLeft | Qt.AlignTop)
			self.box.append( QWidget())
			self.image.append(image)
			label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
			self.label.append(label)

			self.box[i].setLayout(l)
			#self.box[i].setFixedSize(380,80)	#setMinimumSize(400, 500)#
			l.addWidget(self.image[i])
			l.addWidget(self.label[i])

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))

		self.back = QAction(icon_get("go-previous",size=32), _("Back"), self)
		self.back.triggered.connect(self.callback_back)
		toolbar.addAction(self.back)

		self.forward= QAction(icon_get("go-next",size=32), _("Next"), self)
		self.forward.triggered.connect(self.callback_forward)
		toolbar.addAction(self.forward)


		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)


		self.undo = QAction(QIcon(get_icon_path("www")), _("Online help"), self)
		self.undo.setStatusTip(_("On line help"))
		self.undo.triggered.connect(self.on_line_help)
		toolbar.addAction(self.undo)

		self.undo = QAction(icon_get("close",size=32), _("Hide"), self)
		self.undo.setStatusTip(_("Close"))
		self.undo.triggered.connect(self.callback_close)
		toolbar.addAction(self.undo)




		self.vbox.addWidget(toolbar)

		for i in range(0,5):
			self.vbox.addWidget(self.box[i])

		self.vbox.addStretch()

		self.status_bar = QStatusBar()
		self.vbox.addWidget(self.status_bar)
		
		self.setLayout(self.vbox)


	def callback_close(self,widget):
		self.toggle_visible()

	def callback_forward(self,widget):
		self.pos=self.pos+1
		if self.pos>=len(self.last):
			self.pos=len(self.last)-1

		self.update()

	def callback_back(self,widget):
		self.pos=self.pos-1
		if self.pos<0:
			self.pos=0
		self.update()

	def on_line_help(self,widget):
		webbrowser.open(sim_name.web+"/man/index.html")

	def update(self):
		items=int(len(self.last[self.pos])/2)
		for i in range(0,5):
			self.box[i].hide()
		tot_height=0
		line_height=20
		for i in range(0,items):
			all_text=self.last[self.pos][i*2+1]
			nbr=all_text.count("<br>")
			len(all_text.split("<br>")[-1])
			pixmap = QPixmap(get_icon_path(self.last[self.pos][i*2],size=64))
			self.image[i].setPixmap(pixmap)
			text=all_text+"<br>"
			self.label[i].setText(text)
			height=len(all_text)
			tot_height=tot_height+height+nbr*line_height
			
			#self.label[i].setFixedSize(380,300)
			self.label[i].adjustSize()
			self.label[i].setOpenExternalLinks(True)
			self.box[i].show()
			#self.image[i].show()

		#self.resize(300, tot_height+80)	#items*self.item_height

		self.forward.setEnabled(True)
		self.back.setEnabled(True)

		if self.pos==0:
			self.back.setEnabled(False)

		if self.pos==len(self.last)-1:
			self.forward.setEnabled(False)

		self.status_bar.showMessage(str(self.pos)+"/"+str(len(self.last)-1))
		self.adjustSize()

	def help_set_help(self,array):
		add=True
		if len(self.last)!=0:
			if self.last[self.pos][1]==array[1]:
				add=False

		if add==True:
			self.pos=self.pos+1
			self.last.append(array)

		self.update()
		self.move_window()

	def help_append(self,array):
		last_item=len(self.last)-1
		self.last[last_item]=self.last[last_item] + array
		self.update()
		#self.resize(300, 150)
		self.move_window()

def help_init():
	global my_help_class
	my_help_class=help_class()

def help_window():
	global my_help_class
	return my_help_class

def language_advert():
	lang=get_language()
	f=os.path.join(get_flag_file_path(),lang+".png")
	if os.path.isfile(f)==True:
		b=bibtex()
		loaded=b.load(os.path.join(get_full_desired_lang_path(),"ref.bib"))

		if loaded==False or r.author=="":
			my_help_class.help_append([f,"<big><b>"+_("OghmaNano in your language!")+"</b></big><br>"+"Would you like OghmaNano to be translated into your native language?  If so please help with the OghmaNano <a href=\""+sim_name.web+"/translation.html\">translation project.</a>"])
		else:
			my_help_class.help_append([f,"<big><b>"+_("OghmaNano translated by:")+"</b></big><br>"+r.author])
			
