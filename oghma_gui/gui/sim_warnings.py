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

## @package sim_warnings
#  The sim warnings window.
#
#qt
from gui_enable import gui_get
import i18n
_ = i18n.language.gettext
if gui_get()==True:
	from gQtCore import QSize, Qt 
	from PySide2.QtWidgets import QWidget,QLineEdit,QHBoxLayout,QPushButton,QLabel,QDialog,QVBoxLayout,QSizePolicy, QDialogButtonBox,QTextEdit
	from PySide2.QtGui import QPainter,QIcon,QImage, QFont

	from icon_lib import icon_get

	class sim_warnings(QDialog):

		def __init__(self,text):
			QDialog.__init__(self)
			icon=icon_get("icon")
			self.setWindowIcon(icon)
			self.setWindowTitle("Simulation errors") 
			self.setWindowFlags(Qt.WindowStaysOnTopHint)

			self.main_vbox=QVBoxLayout()

			label=QLabel(_("The following erros/warning were found while running the simulations:"))
			label.setFont(QFont('SansSerif', 12))
			label.setWordWrap(True)
			self.main_vbox.addWidget(label)

			self.textbox = QTextEdit(self)
			self.main_vbox.addWidget(self.textbox)
			self.textbox.setText(text)
			self.textbox.setMinimumHeight(330)

			self.btns = QDialogButtonBox()
			self.btns.setStandardButtons( QDialogButtonBox.Ok)
			self.main_vbox.addWidget(self.btns)

			self.btns.accepted.connect(self.accept)
			self.btns.rejected.connect(self.reject)

			self.setLayout(self.main_vbox)

			self.setMinimumWidth(300)
			self.exec_()
else:
	class sim_warnings():
		def __init__(self,text):
			print("sim warnings")
