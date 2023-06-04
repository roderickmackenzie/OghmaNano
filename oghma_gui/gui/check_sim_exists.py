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

## @package check_sim_exists
#  Check the simulation has not been removed.
#

import os
from win_lin import get_platform
from threading import Thread
import i18n
from i18n import get_full_language

_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget
from gQtCore import gSignal
from PySide2.QtWidgets import QWidget

from gQtCore import QTimer

import time

class check_sim_exists(QWidget):
	sim_gone = gSignal()

	def __init__(self):
		QWidget.__init__(self)
		self.sim_dir=""
			
	def foo(self,n):
		count=0
		while(1):
			if self.sim_dir!="":
				if os.path.isdir(self.sim_dir)==False:
					count=count+1
				else:
					count=0

			if count>5:
				self.sim_dir=""
				self.sim_gone.emit()
				count=0

			time.sleep(1)

	def set_dir(self,sim_dir):
		self.sim_dir=sim_dir

	def start_thread(self):
		p = Thread(target=self.foo, args=(10,))
		p.daemon = True
		p.start()

		


