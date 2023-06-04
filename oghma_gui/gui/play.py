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

## @package play
#  A play button
#


#qt
from gQtCore import gSignal
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon, QKeySequence
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit


from icon_lib import icon_get

from util import wrap_text

from server import server_get

from QAction_lock import QAction_lock

class play(QAction_lock):

	start_sim = gSignal()
	stop_sim = gSignal()

	def start(self):
		self.setIcon(icon_get("media-playback-pause"))
		self.setText(_("Stop\nsimulation"))
		self.running=True

	def stop(self):
		self.setIcon(icon_get(self.play_icon))
		self.setText(self.run_text)
		self.running=False

	def do_emit(self):
		pass


		if self.running==False:
			self.start_sim.emit()
		else:
			server_get().killall()


	def __init__(self,parent,id,play_icon="media-playback-start",run_text=_("Run simulation"),connect_to_server=True):
		self.play_icon=play_icon
		self.run_text=run_text
		self.running=False
		QAction_lock.__init__(self,self.play_icon,self.run_text,parent,id)
		self.clicked.connect(self.do_emit)

		if connect_to_server==True:
			server_get().sim_started.connect(self.start)
			server_get().sim_finished.connect(self.stop)


