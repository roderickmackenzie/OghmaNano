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

## @package command_line_tool
#  A command line tool
#

import os
import sys
from sim_name import sim_name

sys.path.append("./gui/")
sys.path.append("./gui/base/")
sys.path.append(os.path.join("/usr/lib",sim_name.install_dir))
sys.path.append(os.path.join("/usr/lib64",sim_name.install_dir))
sys.path.append(os.path.join("/usr/share",sim_name.install_dir,"gui"))	#debian


from gui_enable import gui_test
gui_test()

from cal_path import calculate_paths
from cal_path import calculate_paths_init

calculate_paths_init()
calculate_paths()
from cal_path import get_lang_path

import i18n
_ = i18n.language.gettext

from token_lib import build_token_lib
build_token_lib()

from cal_path import print_paths

from ver import ver_load_info
from ver import ver
from ver import version

from cal_path import test_arg_for_sim_file
from gui_enable import set_gui

import i18n
_ = i18n.language.gettext

import argparse

ver_load_info()


parser = argparse.ArgumentParser(epilog=sim_name.name+" "+_("command line tool")+" "+sim_name.web+"\n"+_("Report bugs to:")+" roderick.mackenzie@oghma-nano.com")
parser.add_argument("--version", help=_("displays the current version"), action='store_true')
parser.add_argument("--ver", help=_("displays the current version"), action='store_true')
parser.add_argument("--paths", help=_("Prints the used paths"), action='store_true')
parser.add_argument("--pvlighthouse_sync", help=_("www.pvlighthouse.com.au sync"), action='store_true')
set_gui(False)

if test_arg_for_sim_file()==False:
	args = parser.parse_args()

def command_args_tool(argc,argv):
	if test_arg_for_sim_file()!=False:
		return
	elif args.pvlighthouse_sync:
		from pvlighthouse import pvlighthouse_sync
		pvlighthouse_sync()
	if argc>=2:
		if args.version:
			print(version())
			sys.exit(0)
		elif args.ver:
			print(ver())
			sys.exit(0)
		elif args.paths:
			print_paths()
			sys.exit(0)
		elif args.token_append:
			device_lib_token_append_after(args.token_append[0],dir_name=args.token_append[1])
			exit(0)



command_args_tool(len(sys.argv),sys.argv)

