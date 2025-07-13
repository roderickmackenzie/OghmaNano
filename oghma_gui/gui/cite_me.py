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
from lock import get_lock
from icon_lib import icon_get
from PySide2.QtGui import QFont
from sim_name import sim_name
import ctypes
from json_c import json_c
from bytes2str import str2bytes
from json_c import json_string

class cite_me(QLabel):

	changed = gSignal()

	def __init__(self):
		QLabel.__init__(self)
		self.all_text=""
		self.setWordWrap(True)
		self.setMinimumWidth(350)
		uid=get_lock().get_uid()
		#FIX
		import random, string
		uid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
		self.bin=json_c("file_defined")
		self.bin.load(os.path.join(sim_paths.get_bib_path(),"cite.bib"))
		single_quote = json_string()
		three_quotes = json_string()
		self.bin.lib.json_py_bib_get_oghma_citations(ctypes.byref(single_quote),ctypes.byref(three_quotes),ctypes.byref(self.bin),ctypes.c_char_p(str2bytes(uid)))

		single_quote=single_quote.get_data()
		self.all_text=three_quotes.get_data()

		self.bin.free()

		self.setText(single_quote)

	def mousePressEvent(self, ev):
		self.win=QWidget()
		self.win.setWindowIcon(icon_get("icon"))
		self.win.setWindowTitle(_("Please cite these papers:")) 
		self.win.setWindowFlags(Qt.WindowStaysOnTopHint)

		vbox=QVBoxLayout()

		l=QLabel(_("If you publish a paper, book or thesis using results from "+sim_name.name+". You <b>must</b> cite these three papers listed below:"))
		l.setFont(QFont('SansSerif', 14))
		l.setWordWrap(True)
		vbox.addWidget(l)

		self.papers = QTextEdit()
		self.papers.setFont(QFont('SansSerif', 11))
		vbox.addWidget(self.papers)
		self.papers.setText(self.all_text)
		
		self.win.setLayout(vbox)

		self.win.setMinimumWidth(400)
		self.win.setMinimumHeight(500)
		self.win.show()


