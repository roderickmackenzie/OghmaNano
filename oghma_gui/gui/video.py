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

import os

from gQtCore import QDir, Qt, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QDesktopWidget
from PySide2.QtWidgets import QWidget, QPushButton, QAction
from PySide2.QtGui import QIcon
from cal_path import sim_paths

class video(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.setMinimumSize(800,520)
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle = self.frameGeometry()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
		self.setWindowTitle("Welcome") 


		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		videoWidget = QVideoWidget()

		self.playButton = QPushButton()
		self.playButton.setEnabled(False)
		self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playButton.clicked.connect(self.play)

		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.setPosition)


		# Create a widget for window contents
		wid = QWidget(self)

		# Create layouts to place inside widget
		controlLayout = QHBoxLayout()
		controlLayout.setContentsMargins(0, 0, 0, 0)
		controlLayout.addWidget(self.playButton)
		controlLayout.addWidget(self.positionSlider)

		layout = QVBoxLayout()
		layout.addWidget(videoWidget)
		layout.addLayout(controlLayout)

		# Set widget to contain window contents
		wid.setLayout(layout)

		self.mediaPlayer.setVideoOutput(videoWidget)
		self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)
		self.mediaPlayer.error.connect(self.handleError)

		self.openFile()
		self.mediaPlayer.play()

		self.setLayout(layout)


	def openFile(self):
		fileName=os.path.join(sim_paths.get_video_path(),"welcome.wmv")
		print(QUrl.fromLocalFile(fileName))
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
		self.playButton.setEnabled(True)


	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
		    self.mediaPlayer.pause()
		else:
		    self.mediaPlayer.play()

	def mediaStateChanged(self, state):
		if self.mediaPlayer.state()==0:
			self.close()
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
		    self.playButton.setIcon(
		            self.style().standardIcon(QStyle.SP_MediaPause))
		else:
		    self.playButton.setIcon(
		            self.style().standardIcon(QStyle.SP_MediaPlay))

	def positionChanged(self, position):
		self.positionSlider.setValue(position)

	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)

	def setPosition(self, position):
		self.mediaPlayer.setPosition(position)

	def handleError(self):
		self.playButton.setEnabled(False)
		print("Error: " + self.mediaPlayer.errorString())

