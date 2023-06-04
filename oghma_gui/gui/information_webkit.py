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

## @package information_webkit
#  Information about gpvdm if we have webkit installed.
#

from tab_base import tab_base
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout,QProgressBar,QLabel,QDesktopWidget,QToolBar,QHBoxLayout,QAction,QSizePolicy,QLineEdit
from PySide2.QtGui import QPixmap
from qQtWebKitWidgets import QWebView
from sim_name import sim_name

class information(QWidget,tab_base):

	def update_buttons(self):
		self.url_bar.set_text( widget.get_main_frame().get_uri() )
		self.back_button.set_sensitive(self.web.can_go_back())
		self.forward_button.set_sensitive(self.web.can_go_forward())

	def update(self):
		print("")
		
	def browse(self):

		url = self.tb_url.text()
		if url.count("://")==0:
		    url = "http://"+url
		self.tb_url.setText(url)

		self.html.load(QUrl(url))

	def home(self):
		self.tb_url.setText(self.default_url)
		self.browse()

	def __init__(self):
		QWidget.__init__(self)

		self.setMinimumSize(1000,500)
		self.html = QWebView()

		vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))

		back = QAction(icon_get("go-previous.png"),  _("back"), self)
		back.triggered.connect(self.html.back)
		toolbar.addAction(back)

		home = QAction(icon_get("user-home.png"),  _("home"), self)
		home.triggered.connect(self.home)
		toolbar.addAction(home)

		self.tb_url=QLineEdit()
		self.tb_url.returnPressed.connect(self.browse)
		toolbar.addWidget(self.tb_url)
		
		vbox.addWidget(toolbar)

		self.default_url = sim_name.web+"/welcome.html"
		self.tb_url.setText(self.default_url)
		self.browse()

		vbox.addWidget(self.html)

		self.setLayout(vbox)
		return

