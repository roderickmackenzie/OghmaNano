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

## @package tab_lang
#  A tab to select the language used.
#


from token_lib import tokens
from undo import undo_list_class
from tab_base import tab_base
from util import latex_to_html
from cal_path import get_share_path
from help import help_window

from PySide2.QtWidgets import QWidget, QScrollArea,QVBoxLayout,QProgressBar,QLabel,QDesktopWidget,QToolBar,QHBoxLayout,QAction, QSizePolicy, QTableWidget, QTableWidgetItem,QComboBox,QDialog,QAbstractItemView,QGridLayout,QLineEdit

import i18n
from i18n import get_languages
_ = i18n.language.gettext

from error_dlg import error_dlg
from json_local_root import json_local_root
from sim_name import sim_name

class language_tab_class(QWidget,tab_base):

	def __init__(self):
		QWidget.__init__(self)
		self.vbox=QVBoxLayout()

		self.tab=QHBoxLayout()
		widget=QWidget()
		widget.setLayout(self.tab)

		title_label=QLabel()
		title_label.setWordWrap(True)
		title_label.setOpenExternalLinks(True)
		title_label.setText(latex_to_html("<font size=5><b>Select the language you would like use.</b><br><br> If a translation to your language does not exist or could be improved, then please consider joining the <a href=\""+sim_name.web+"/translation.html\"> translation project</a>.  I would like "+sim_name.name+" translated into as many langauges as possible to improve access to high quality solar cell simulation tools for all.</font>"))

		self.vbox.addWidget(title_label)
		self.vbox.addWidget(widget)


		description=QLabel()
		description.setText(latex_to_html("Default language:"))

		self.lang_box=QComboBox()


		self.lang_box.addItem("auto")

		self.lang_box.setFixedSize(300, 25)


		self.tab.addWidget(description)
		self.tab.addWidget(self.lang_box)
		


		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.vbox.addWidget(spacer)
		self.setLayout(self.vbox)

		langs=get_languages()
		if langs==False:
			return

		for i in range(0,len(langs)):
			self.lang_box.addItem(langs[i])
		local=json_local_root()
		token=local.international.lang
		all_items  = [self.lang_box.itemText(i) for i in range(self.lang_box.count())]
		for i in range(0,len(all_items)):
			if all_items[i] == token:
				self.lang_box.setCurrentIndex(i)
				
		self.lang_box.currentIndexChanged.connect(self.callback_edit)

	def callback_edit(self):
		local=json_local_root()
		local.international.lang=self.lang_box.itemText(self.lang_box.currentIndex())
		local.save()
		error_dlg(self,"Please restart the software for the changes to take effect.")

	def help(self):
		help_window().get_help(self.file_name)


