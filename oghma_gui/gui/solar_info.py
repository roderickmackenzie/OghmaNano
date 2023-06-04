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

## @package solar_info
#  not needed.
#

from PySide2.QtWidgets import QWidget,QMessageBox


class infoBox(QWidget):
    def __init__(self, parentObject, parent=None):
        super(infoBox, self).__init__(parent)
        self.parentObject = parentObject

        if parentObject.enable_earthattr:
            text = "Earth's Atmosphere contains approximately 78% Nitrogen, 21% oxygen, and small amounts of other " \
                   "elements.\n\n" \
                   "The sun's radiation is absorbed by various substances in the stmosphere, including water vapour, " \
                   "ozone, and dust particles.\n\n " \
                   "This model assumes cloudless skies."

        if parentObject.enable_mercuryattr:
            text = 'Mercury has no atmosphere, and therefore none of the incoming solar radiation is absorbed.\n\n' \
                   'The solar spectrum reaching the surface of Mercury is the extra-terrestial spectrum, corrected ' \
                   'for distance from the sun.'

        if parentObject.enable_venusattr:
            text = 'yoyrrrrroyo'

        if parentObject.enable_marsattr:
            text = "The Martian atmosphere consists of mostly carbon dioxide (96%), and small amounts of other " \
                   "gases.\n\n It has a mean pressure of approximately 0.6% that of Earth's at sea level. Incoming " \
                   "solar radiation is absorbed by carbon dioxide (in the 2 micron + range), and aerosols such as " \
                   "Martian dust."

        if parentObject.enable_ceresattr:
            text = "There are indications that Ceres has a tenuous atmosphere of water vapour caused by sublimation " \
                   "of ice from the surface. This is unproved however, and likely negligible, therefore he solar" \
                   " spectrum reaching the surface of Ceres is the extra-terrestial spectrum, corrected for distance " \
                   "from the sun. "

        if parentObject.enable_europaattr:
            text = "Europa has a very tenuous atmosphere composed solely of molecular oxygen, offerring little " \
                   "protection from the sun's radiation. It has an atmospheric pressure 10^(-12) times less than" \
                   " that of Earth, having a negligible effect on the incoming radiation."

        if parentObject.enable_halleyattr:
            text = "Halley's comet has no atmosphere, but when it's orbit takes it close to the sun the comet" \
                   " develops a coma up to 100,000 km across. Evaporation of this dirty ice releases dust " \
                   "particles, which travel with the gas away from the nucleus. Gas molecules in the coma absorb " \
                   "solar light and then re-radiate it at different wavelengths, a phenomenon known as " \
                   "fluorescence, whereas dust particles scatter the solar light. Both processes are responsible " \
                   "for making the coma visible."

        if parentObject.enable_plutoattr:
            text = "PLuto has a very tenuous atmosphere roughly 100,000 times less dense than the Earth's atmosphere." \
                   ""

        d = QMessageBox()
        d.setWindowTitle('Information')
        # d.setIcon(QMessageBox.Information)
        d.setText(text)
        d.exec_()
