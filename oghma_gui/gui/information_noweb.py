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

## @package information_noweb
#  Information about gpvdm if we do not have webkit installed.
#

import os
from help import my_help_class

import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon,QPixmap,QPalette
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QScrollArea,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar, QMessageBox, QVBoxLayout, QGroupBox, QTableWidget,QAbstractItemView, QTableWidgetItem, QLabel
from cal_path import sim_paths

class information(QScrollArea):

	def __init__(self,file_name):
		QScrollArea.__init__(self)
		self.main_widget=QWidget()

		hbox=QHBoxLayout()
		self.setStyleSheet("background-color:white;");
		self.label = QLabel()

		self.label.setAlignment(Qt.AlignTop)
		self.label.setOpenExternalLinks(True);
		self.label.setWordWrap(True)

		html_file=os.path.join(sim_paths.get_html_path(),file_name)
		text="File not found"
		if os.path.isfile(html_file)==True:
			f = open(os.path.join(sim_paths.get_html_path(),file_name), encoding='utf-8')
			data = f.readlines()
			f.close()
			text=""
			for i in range(0, len(data)):
				line=data[i]
				line=bytes(line, 'utf-8').decode('utf-8', 'ignore')
				text=text+'\n'+data[i].rstrip()

			text=text.replace("get_image_file_path()",sim_paths.get_image_file_path())

		self.label.setText(text)

		hbox.addWidget(self.label)


		self.main_widget.setLayout(hbox)
		self.main_widget.show()
		self.setWidget(self.main_widget)

	def update(self):
		print("")
		


