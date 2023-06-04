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

#qt
try:
	from PySide2.QtWidgets import QMessageBox
except:
	pass


def yes_no_cancel_dlg(parent,text):
	if parent!=None:
		msgBox = QMessageBox(parent)
		msgBox.setIcon(QMessageBox.Question)
		msgBox.setText("Question")
		msgBox.setInformativeText(text)
		msgBox.setStandardButtons(QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel  )
		msgBox.setDefaultButton(QMessageBox.No)
		reply = msgBox.exec_()
		if reply == QMessageBox.Yes:
			return "yes"
		elif reply == QMessageBox.No:
			return "no"
		else:
			return "cancel"
	else:
		reply = input(text+"y/n/c")

		if reply == "y":
			return "yes"
		elif reply == "n":
			return "no"
		else:
			return "cancel"
		
