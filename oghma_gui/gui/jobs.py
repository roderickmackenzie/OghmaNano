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

from inp import inp_search_token_value
from status_icon import status_icon_stop


#qt
from gQtCore import QSize, Qt
from PySide2.QtGui import QIcon,QPalette
from PySide2.QtWidgets import QWidget, QVBoxLayout,QProgressBar,QLabel,QDesktopWidget,QToolBar,QHBoxLayout,QAction, QSizePolicy,  QTableWidgetItem,QComboBox,QDialog,QAbstractItemView

from PySide2.QtGui import QPixmap
from gQtCore import gSignal
from PySide2.QtWidgets import QWidget

from server import server_get

from g_tab import g_tab
import time

## @package jobs
#  A jobs viewer widget.
#

class jobs_view(QWidget):

	def __init__(self):
		QWidget.__init__(self)

		self.main_vbox=QVBoxLayout()
	
		self.tab = g_tab()
		self.tab.resizeColumnsToContents()

		self.tab.verticalHeader().setVisible(False)

#		self.tab.cellChanged.connect(self.tab_changed)
		
		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)

		self.myserver=server_get()
		self.myserver.jobs_update.connect(self.callback_cluster_get_jobs)

		self.show()

	def callback_cluster_get_jobs(self):

		self.tab.clear()
		self.tab.setColumnCount(7)
		self.tab.setRowCount(0)
		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tab.setHorizontalHeaderLabels([ _("name"), _("path"), _("ip"), _("start"), _("stop"), _("CPUs"), _("status")])


		for job in self.myserver.jobs:
			start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job.start_time))
			self.tab.add([job.name,job.path,job.ip,start_time,job.stop,str(job.cpus),str(job.status)])








