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

## @package cite_me
#  A widget to encourage people to cite the model
#


import os

#qt
from PySide2.QtWidgets import QLabel, QFrame,QTextEdit, QComboBox,  QDialog, QVBoxLayout , QDialogButtonBox, QTextEdit,QWidget,QHBoxLayout,QSizePolicy
from PySide2.QtGui import QPixmap, QIcon
from gQtCore import QSize, Qt, QTimer, QPersistentModelIndex, gSignal
from QComboBoxLang import QComboBoxLang

#cal_path
from cal_path import sim_paths
from epitaxy import get_epi
from inp import inp
from dos_io import gen_fermi_from_np
from dos_io import gen_np_from_fermi
from bibtex import bibtex
from lock import get_lock
from icon_lib import icon_get
from PySide2.QtGui import QFont
from sim_name import sim_name

class cite_me(QLabel):

	changed = gSignal()

	def gen_window(self):
		self.win=QWidget()
		self.win.setWindowIcon(icon_get("icon"))
		self.win.setWindowTitle(_("Please cite these papers:")) 
		self.win.setWindowFlags(Qt.WindowStaysOnTopHint)

		vbox=QVBoxLayout()

		l=QLabel(_("If you publish a paper, book or thesis using results from "+sim_name.name+". You must cite these three papers listed below:"))
		l.setFont(QFont('SansSerif', 14))
		l.setWordWrap(True)
		vbox.addWidget(l)

		self.papers = QTextEdit()
		vbox.addWidget(self.papers)
		self.papers.setText(self.all_text)
		
		self.win.setLayout(vbox)

		self.win.setMinimumWidth(350)
		#self.win.setMinimumHeight(500)
		self.win.show()

		
	def __init__(self):
		QLabel.__init__(self)
		self.all_text=""
		self.setWordWrap(True)
		self.setMinimumWidth(350)
		bib=bibtex()
		#try:
		bib.load(os.path.join(sim_paths.get_bib_path(),"cite.bib"))

		number=sum(ord(c) for c in get_lock().get_uid()) %10

		if number<len(bib.refs):
			text=bib.refs[number].bib_short_cite()
			count=0
			pos=number
			while count<3:
				self.all_text=self.all_text+str(count+1)+". "+bib.refs[pos].bib_short_cite()+"\n\n"
				count=count+1
				pos=pos+1
				if pos>len(bib.refs):
					pos=0
			self.all_text=self.all_text+"\n"+"Please do not cite the manual.  See the manual why I ask you to cite in this way. Thank you!"

			self.setText("<b>If you publish results generated with OghmaNano in a paper, book or thesis you must cite this paper:</b> "+text+" and along with these <a href=\"https://scholar.google.co.uk/citations?user=jgQqfLsAAAAJ&hl=en\">two papers</a> in your work.")
		#except:
		#	pass

	def mousePressEvent(self, ev):
		self.gen_window()


