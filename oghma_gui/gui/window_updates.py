# 
#   General-purpose Photovoltaic Device Model - a drift diffusion base/Shockley-Read-Hall
#   model for 1st, 2nd and 3rd generation solar cells.
#   Copyright (C) 2012-2017 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.gpvdm.com
#   Room B86 Coates, University Park, Nottingham, NG7 2RD, UK
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License v2.0, as published by
#   the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# 

## @package update
#  Check for updates.
#

import os
from threading import Thread

#qt
from PySide2.QtGui import QIcon, QColor
from gQtCore import QSize, Qt,QFile,QIODevice,QTimer
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QTableWidget, QAbstractItemView, QStatusBar, QTableWidgetItem

from gui_util import yes_no_dlg
from icon_lib import icon_get

from process_events import process_events
from msg_dlg import msg_dlg

from QAction_lock import QAction_lock
from gQtCore import gSignal

import i18n
_ = i18n.language.gettext

import ctypes
from cal_path import sim_paths
from progress_class import progress_class
from datetime import datetime
from bytes2str import bytes2str

CALLBACKFUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

class update_item(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char * 200),
		("web_path", ctypes.c_char * 4096),
		("web_path_json", ctypes.c_char * 4096),
		("local_path", ctypes.c_char * 4096),
		("local_path_json", ctypes.c_char * 4096),
		("local_time", ctypes.c_longlong),
		("remote_time", ctypes.c_longlong),
		("local_checksum", ctypes.c_char * 50),
		("remote_checksum", ctypes.c_char * 50),
		("downloaded", ctypes.c_int),
		("remote_size", ctypes.c_int),
		("local_size", ctypes.c_int),
		("installed", ctypes.c_int),
		("repository_type", ctypes.c_int),
	]

class updates(ctypes.Structure):
	_fields_ = [
		("nfiles", ctypes.c_int),
		("max_files", ctypes.c_int),
		("items", ctypes.POINTER(update_item)),
		("percent", ctypes.c_int),
		("message", ctypes.c_char * 4096),
		("callback", CALLBACKFUNC),
	]

class window_updates(QWidget):
	got_updates = gSignal()
	got_message = gSignal(str)

	def __init__(self):
		QWidget.__init__(self)
		self.lib=sim_paths.get_dll_py()
		self.setMinimumWidth(1000)
		self.setMinimumHeight(800)

		self._cb = CALLBACKFUNC(self._static_callback)
		self.updates=updates()
		self.updates.callback = self._cb

		self.lib.updates_init(ctypes.byref(self.updates))
		self.lib.updates_populate(ctypes.byref(self.updates),ctypes.byref(sim_paths))

		self.vbox=QVBoxLayout()

		self.setWindowTitle(_("Updater")+" (https://www.oghma-nano.com)")

		toolbar=QToolBar()

		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.tb_update = QAction_lock("update", _("Update"), self,"update")
		self.tb_update.clicked.connect(self.download_updates)
		toolbar.addAction(self.tb_update)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.progress=progress_class()
		self.progress.spinner.stop()
		#self.progress.spinner.hide()
		#self.progress.set_text("")
		#self.progress.hide_time()

		self.vbox.addWidget(toolbar)

		self.tab = QTableWidget()
		self.tab.resizeColumnsToContents()

		self.tab.verticalHeader().setVisible(False)

		
		self.tab.setColumnCount(6)
		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		#self.tab.setColumnWidth(3, 200)

		self.tab.verticalHeader().setVisible(False)
		
		#self.select_param_window=select_param(self.tab)
		#self.select_param_window.set_save_function(self.save_combo)

		#self.create_model()

		#self.tab.cellChanged.connect(self.tab_changed)

		self.vbox.addWidget(self.tab)

		self.status_bar=QStatusBar()
		self.vbox.addWidget(self.status_bar)		

		self.setLayout(self.vbox)
		self.show_updates()
		#self.update.update_progress.connect(self.update_progress)
		self.got_updates.connect(self.show_updates)
		self.got_message.connect(self.callback_show_message)
		self.update_check()
		self.setWindowIcon(icon_get("update"))


	def update_progress(self,line,percent):
		return
		if self.isVisible()==True:
			if line!=-1:
				self.tab.setItem(line,5,QTableWidgetItem(str(self.update.file_list[line].get_status())))
				self.tab.setItem(line,4,QTableWidgetItem(str(self.update.file_list[line].md5_disk)))
				self.tab.selectRow( line );

		#self.progress.set_fraction(percent)
		#self.progress.set_text(self.update.get_progress_text())
		process_events()


	def format_size(self, val):
		ret_str = ctypes.create_string_buffer(20)
		self.lib.file_size_with_units(ret_str,  ctypes.c_int(val))
		return ret_str.value.decode('utf-8')

	def extract_domain(self,url):
		if url.startswith("https://"):
			url = url[len("https://"):]
		elif url.startswith("http://"):
			url = url[len("http://"):]

		# Split at the first slash to get the domain
		domain = url.split("/")[0]
		return domain

	def show_updates(self):
		self.status_bar.showMessage("")
		self.tab.blockSignals(True)
		self.tab.clear()
		self.tab.setRowCount(0)

		# Set column widths and headers
		self.tab.setColumnCount(5)
		self.tab.setColumnWidth(0, 150)
		self.tab.setColumnWidth(1, 200)
		self.tab.setColumnWidth(2, 200)
		self.tab.setColumnWidth(3, 100)
		self.tab.setColumnWidth(4, 100)
		self.tab.setColumnWidth(5, 100)
		self.tab.setHorizontalHeaderLabels([
			_("Name"),  _("Server"), _("Update issued"), _("Remote Size"), _("Status")
		])

		# Loop through the files in the ctypes structure
		self.tb_update.setEnabled(False)
		all_upto_date=True
		for i in range(self.updates.nfiles):
			item = self.updates.items[i]
			pos = self.tab.rowCount()
			self.tab.insertRow(pos)
			dt = datetime.utcfromtimestamp(item.remote_time)
			formatted = dt.strftime("%d/%m/%Y")
			self.tab.setItem(pos, 0, QTableWidgetItem(item.name.decode('utf-8')))
			self.tab.setItem(pos, 1, QTableWidgetItem(self.extract_domain(item.web_path.decode('utf-8'))))
			self.tab.setItem(pos, 2, QTableWidgetItem(formatted))
			self.tab.setItem(pos, 3, QTableWidgetItem(self.format_size(item.remote_size)))

			status_str = "Installed" if item.installed else "Not Installed"
			self.tab.setItem(pos, 4, QTableWidgetItem(status_str))

			status_item = self.tab.item(pos, 4)
			if "installed" == status_str.lower():
				status_item.setForeground(QColor("green"))
			else:
				all_upto_date=False
				status_item.setForeground(QColor("red"))

		if all_upto_date==False:
			self.tb_update.setEnabled(True)

		self.tab.blockSignals(False)
		self.status_bar.showMessage("")
		self.tab.setEnabled(True)

	def thread_get_updates(self):
		self.lib.updates_check(ctypes.byref(self.updates))
		self.got_updates.emit()

	def thread_download_updates(self):
		self.lib.updates_get(ctypes.byref(self.updates))
		self.lib.updates_install(ctypes.byref(sim_paths),ctypes.byref(self.updates))
		#self.lib.updates_dump(ctypes.byref(self.updates))
		self.got_updates.emit()

	def update_check(self):
		self.status_bar.showMessage("Checking for updates.....")
		self.update_check_thread = Thread(target=self.thread_get_updates)
		self.update_check_thread.daemon = True
		self.update_check_thread.start()
		self.progress.show()
		self.progress.start()
		self.tab.setEnabled(False)

	def download_updates(self):
		self.status_bar.showMessage("Downloading updates.....")
		p = Thread(target=self.thread_download_updates)
		p.daemon = True
		p.start()
		self.progress.show()
		self.progress.start()

	def _static_callback(self, msg):
		# Delegate to the instance method
		#self.my_callback(msg)
		self.got_message.emit(bytes2str(msg))

	def callback_show_message(self,msg):
		if msg=="finish":
			self.progress.close()

		text=bytes2str(ctypes.cast(self.updates.message, ctypes.c_char_p).value)
		self.progress.set_fraction(float(self.updates.percent)/100.0)
		self.progress.set_text(text)
		#self.status_bar.showMessage(text)

