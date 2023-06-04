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

## @package command_args
#  Handle command line arguments.
#

import sys
import os

from scan_io import scan_io
from const_ver import const_ver

from cal_path import get_exe_command
from dat_file import dat_file
from scan_plot import scan_gen_plot_data
from win_lin import get_platform
from cal_path import test_arg_for_sim_file
from cal_path import set_sim_path

from gui_enable import set_gui
from gui_enable import gui_get
from sim_name import sim_name
import i18n
_ = i18n.language.gettext

import argparse
parser = argparse.ArgumentParser(epilog=_("Additional information about gpvdm is available at")+" "+sim_name.web+"\n"+_("Report bugs to:")+" roderick.mackenzie@oghma-nano.com")
parser.add_argument("--version", help=_("displays the current version"), action='store_true')
parser.add_argument("--ver", help=_("displays the current version"), action='store_true')
parser.add_argument("--cleanscandirs", help=_("Deletes the content of all scan directories."), nargs=1)
parser.add_argument("--load", help=_("Loads a simulation --load /path/containing/simulation/sim.oghma"), nargs=1)
parser.add_argument("--unpack", help=_("Extract the sim.oghma archive --unpack"), action='store_true')
parser.add_argument("--pack", help=_("Extract the sim.oghma archive --pack"), action='store_true')

if test_arg_for_sim_file()==False:
	args = parser.parse_args()

def command_args(argc,argv):
	if test_arg_for_sim_file()!=False:
		return

	if argc>=2:
		if args.version:
			print(const_ver())
			sys.exit(0)
		elif args.ver:
			print(const_ver())
			sys.exit(0)
		elif args.cleanscandirs:
			scan=scans_io(os.getcwd())
			scan.clean_all()
			sys.exit(0)
		elif args.load:
			set_sim_path(os.path.dirname(args.load[0]))

