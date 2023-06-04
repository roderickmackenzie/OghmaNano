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

## @package report_error
#  Report an error using a thread.
#

from win_lin import get_platform
from threading import Thread

import i18n
_ = i18n.language.gettext
from const_ver import const_ver

#qt
from gQtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPixmap
from gQtCore import gSignal
from PySide2.QtWidgets import QWidget

from gQtCore import QTimer
from lock import get_lock

class report_error(QWidget):
	reported = gSignal(bool)

	def __init__(self):
		QWidget.__init__(self)
		self.error=""

	def tx_error(self,n):
		get_lock().report_bug(self.error)
		self.reported.emit(True)

	def set_error(self,error):
		self.error=error

	def start(self):
		p = Thread(target=self.tx_error, args=(10,))
		p.daemon = True
		p.start()		


