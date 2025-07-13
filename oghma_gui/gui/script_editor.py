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

## @package script_editor
#  A script editor widget
#


import os

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QShortcut
from PySide2.QtGui import QIcon, QTextFormat,QTextOption, QKeySequence
from gQtCore import QSize, Qt,QFile,QIODevice,QRect
from PySide2.QtWidgets import QWidget,QSizePolicy, QPlainTextEdit,QVBoxLayout,QHBoxLayout, QPushButton,QDialog,QFileDialog,QToolBar, QMessageBox, QLineEdit, QToolButton
from PySide2.QtWidgets import QTabWidget

from PySide2.QtGui import QPainter,QColor
from icon_lib import icon_get

from gQtCore import QFile, QRegExp, Qt
from PySide2.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from code_editor import code_editor

from inp import inp_load_file
import imp
from gQtCore import gSignal

class Highlighter(QSyntaxHighlighter):

	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)

		self.highlightingRules = []

		keyword = QTextCharFormat()
		keyword.setForeground( Qt.darkRed )
		keyword.setFontWeight( QFont.Bold )
		#python
		#keywords = [ "break", "else", "for", "if", "in"
		#			 "next", "repeat", "return", "switch",
		#			 "try", "while","self" ] 
		#lua
		keywords = [ "break", "else", "for", "if", "in"
					 "next", "repeat", "return", "switch",
					 "try", "while","then","end" ] 
		for word in keywords:
			pattern = QRegExp("\\b" + word + "\\b")
			self.highlightingRules.append( (pattern, keyword) )


		keywords = [ "class","def"]

		for word in keywords:
			pattern = QRegExp(word + "\\b")
			self.highlightingRules.append( (pattern, keyword) )


		keywords = [ "import", "from" ] 
		classFormat = QTextCharFormat()
		classFormat.setForeground(Qt.red)
		for k in keywords:
			self.highlightingRules.append((QRegExp(k+"\\b"),classFormat))


		classFormat = QTextCharFormat()
		classFormat.setFontWeight(QFont.Bold)
		classFormat.setForeground(Qt.darkMagenta)
		self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),classFormat))

		singleLineCommentFormat = QTextCharFormat()
		singleLineCommentFormat.setForeground(Qt.darkBlue)
		self.highlightingRules.append((QRegExp("#[^\n]*"),singleLineCommentFormat))

		self.multiLineCommentFormat = QTextCharFormat()
		self.multiLineCommentFormat.setForeground(Qt.red)

		quotationFormat = QTextCharFormat()
		quotationFormat.setForeground(Qt.darkMagenta)
		self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))

		functionFormat = QTextCharFormat()
		functionFormat.setFontItalic(True)
		functionFormat.setForeground(Qt.blue)
		self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),functionFormat))

		self.commentStartExpression = QRegExp("/\\*")
		self.commentEndExpression = QRegExp("\\*/")

	def highlightBlock(self, text):
		for pattern, format in self.highlightingRules:
		    expression = QRegExp(pattern)
		    index = expression.indexIn(text)
		    while index >= 0:
		        length = expression.matchedLength()
		        self.setFormat(index, length, format)
		        index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		startIndex = 0
		if self.previousBlockState() != 1:
		    startIndex = self.commentStartExpression.indexIn(text)

		while startIndex >= 0:
		    endIndex = self.commentEndExpression.indexIn(text, startIndex)

		    if endIndex == -1:
		        self.setCurrentBlockState(1)
		        commentLength = len(text) - startIndex
		    else:
		        commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

		    self.setFormat(startIndex, commentLength,
		            self.multiLineCommentFormat)
		    startIndex = self.commentStartExpression.indexIn(text,
		            startIndex + commentLength);

class script_editor(code_editor):
	status_changed = gSignal()
	save_signal = gSignal()
	def __init__(self,):
		code_editor.__init__(self)
		font = QFont()
		font.setFamily('Monospace')
		font.setFixedPitch(True)
		font.setPointSize(17)

		self.setFont(font)

		self.highlighter = Highlighter(self.document())
		self.textChanged.connect(self.callback_edit)
		shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
		shortcut.activated.connect(self.save)

		self.not_saved=False
		self.api_callback=None

	def callback_edit(self):

		self.not_saved=True
		self.status_changed.emit()

	def load(self,file_name):
		self.blockSignals(True)
		self.file_name=file_name
		lines=inp_load_file(file_name)
		self.setPlainText("\n".join(lines))
		self.blockSignals(False)

	def setText(self,text):
		self.blockSignals(True)
		self.setPlainText(text)
		self.blockSignals(False)

	def getText(self):
		return self.toPlainText()

	def save(self):
		self.save_signal.emit()


