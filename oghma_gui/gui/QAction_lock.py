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

## @package ribbon_sim_mode
#  The sim mode ribbon.
#


from cal_path import get_css_path

#qt
from PySide2.QtWidgets import QTextEdit, QAction
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QToolBar, QToolButton,QDialog

from gQtCore import gSignal
from icon_lib import icon_get

from msg_dlg import msg_dlg

from lock import get_lock
from lock_trial import lock_trial
from sim_name import sim_name
class QAction_lock(QAction):
	clicked=gSignal(QAction)

	def __init__(self,icon_name,text,s,id):
		sub_icon=None
		self.locked=False
		self.text=text
		
		if get_lock().is_function_locked(id)==True:
			self.locked=True

		if self.locked==True:
			sub_icon="lock"
		QAction.__init__(self,icon_get(icon_name,sub_icon=sub_icon), text, s)
		self.triggered.connect(self.callback_secure_click)

	def callback_secure_click(self):
		if self.locked==False:
			self.clicked.emit(self)
		else:
			self.setChecked(False)

			self.trial=lock_trial(override_text="<br><br><br><br>Upgrade today to "+sim_name.name+" professional to use this function!.<br><br><br>",show_text=False,title_font_size=14)
			self.trial.title_text.setAlignment(Qt.AlignCenter)
			ret=self.trial.run()
			if ret==QDialog.Accepted:
				msgBox = msg_dlg()
				msgBox.setText("Thank you for buying "+sim_name.name+" - please restart "+sim_name.name+" to enable the new features")
				msgBox.exec_()


