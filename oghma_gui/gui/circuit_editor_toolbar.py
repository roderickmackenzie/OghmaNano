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

## @package circuit
#  Widget to draw circuit diagram
#

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar, QFrame, QScrollArea
from PySide2.QtWidgets import QPushButton, QLabel
from PySide2.QtGui import QPainter,QIcon,QPixmap
from ersatzschaltbild import ersatzschaltbild
from icon_lib import icon_get
import functools
from gui_util import yes_no_dlg
from cal_path import sim_paths
from icon_lib import icon_get
from gQtCore import gSignal, QRectF
from PySide2.QtGui import QPainter, QColor, QBrush, QLinearGradient

class ClickableWidget(QWidget):

	def __init__(self, callback_click, icon_name, text, parent=None):
		super().__init__(parent)
		self.icon_name=icon_name
		self.callback_click=callback_click
		#QWidget.__init__(self)

		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.setStyleSheet("QWidget { border: none; padding: 5px; }")

		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(5)

		self.button = QPushButton()
		self.button.setIcon(icon_get(icon_name))
		self.button.setIconSize(QSize(32, 32))
		self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.button.setStyleSheet("QPushButton { border: none; }")

		self.label = QLabel(text)
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		layout.addWidget(self.button)
		layout.addWidget(self.label)

		self.button.clicked.connect(self.handle_click)
		self.label.mousePressEvent = self.handle_click

		#self.setStyleSheet("QWidget { border: none; padding: 5px; background-color: lightblue; }")
        # Define your gradient
	#	gradient = QLinearGradient(0, 0, 0, self.height())
	#	gradient.setColorAt(0, QColor(255, 0, 0))  # Start color
	#	gradient.setColorAt(1, QColor(0, 0, 255))  # End color

	#	self.gradient_brush = QBrush(gradient)

	#def paintEvent(self, event):
	#	painter = QPainter(self)
	#	painter.setBrush(self.gradient_brush)
	#	painter.drawRect(self.rect())

	def handle_click(self, event):
		self.callback_click(self,self.icon_name)

class CollapsiblePanel(QFrame):
	#clicked = gSignal(str)
	def __init__(self, title, items,callback_click,visible=False):
		#super(CollapsiblePanel, self).__init__(parent)
		QFrame.__init__(self)
		self.setFrameShape(QFrame.NoFrame)
		self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)

		self.toggle_button = QPushButton(title)
		self.toggle_button.setCheckable(True)
		self.toggle_button.setChecked(False)
		self.toggle_button.setStyleSheet(
			"QPushButton { text-align: left; padding: 10px; border: none; border-bottom: 1px solid #ccc; }"
			"QPushButton:checked { background-color: #ddd; }"
		)
		self.toggle_button.clicked.connect(self.on_toggle)

		self.content_area = QWidget()
		self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.content_area.setVisible(False)

		self.content_layout = QVBoxLayout(self.content_area)
		self.content_layout.setContentsMargins(10, 0, 0, 0)
		self.content_layout.setSpacing(5)

		for icon_path, text in items:
			clickable_widget = ClickableWidget(callback_click, icon_path, text)
			self.content_layout.addWidget(clickable_widget)
			#clickable_widget.clicked.connect(parent.on_item_click)

		self.layout.addWidget(self.toggle_button)
		self.layout.addWidget(self.content_area)
		if visible==True:
			self.toggle_button.setChecked(True)
			self.content_area.setVisible(True)

		#parent.clicked.connect(self.clicked)
		#

	def on_toggle(self):
		checked = self.toggle_button.isChecked()
		self.content_area.setVisible(checked)

class circuit_editor_toolbar(QWidget):
	clicked = gSignal(str)
	def __init__(self):
		super().__init__()

		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)

		content_widget = QWidget()
		scroll_area.setWidget(content_widget)

		layout = QVBoxLayout(content_widget)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		# Create panels with icons and text
		section1 = CollapsiblePanel(_("Basic"), [
			("resistor", _("Resistor")),
			("capacitor", _("Capacitor")),
			("wire", _("Wire")),
			("ground", _("Ground")),
			("bat", _("Voltage source")),
		],self.button_clicked,visible=True)


		section2 = CollapsiblePanel(_("Non-linear"), [
			("diode", _("Diode")),
			("power", _("Power law")),
			("barrier", _("Barrier")),
			("diode_n", _("Multi diode")),
			("diode_ns1", _("Multi diode+S ")),
			("diode_ns2", _("Multi diode+S (||)")),
		],self.button_clicked)

		section3 = CollapsiblePanel(_("Tools"), [
			("pointer", _("Pointer")),
			("all-scroll", _("Scroll")),
			("clean", _("Clean")),
		],self.button_clicked,visible=True)


		layout.addWidget(section1)
		layout.addWidget(section2)
		layout.addWidget(section3)
		layout.addStretch(1)

		layout = QVBoxLayout()
		layout.addWidget(scroll_area)
		self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
		self.setLayout(layout)
		#self.setCentralWidget(scroll_area)

		self.highlighted_button = None  # Attribute to keep track of the highlighted button


	def button_clicked(self, widget,text):
		if self.highlighted_button:
			self.highlighted_button.setStyleSheet("QWidget { border: none; padding: 5px; }")
		widget.setStyleSheet("QWidget { border: none; padding: 5px; background-color: lightblue; }")
		self.highlighted_button = widget
		self.clicked.emit(text)
