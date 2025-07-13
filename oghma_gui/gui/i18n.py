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

## @package i18n
#  localization back end.
#

import os
import locale
import gettext
from cal_path import sim_paths
from json_c import json_local_root

bin_local=json_local_root()

lang=bin_local.get_token_value("international","lang")

if lang=="auto":
	current_locale, encoding = locale.getdefaultlocale()
	if current_locale==None:
		print("No local language set assuming en_US")	
		current_locale="en_US"
else:
	current_locale=lang
#print(current_locale,sim_paths.get_lang_path())
language = gettext.translation ('oghmanano', sim_paths.get_lang_path(), [current_locale], fallback=True )
language.install()
locale.setlocale(locale.LC_NUMERIC, "C")


def get_language():
	lang=current_locale.split("_")[1].lower()
	return lang

def get_full_language():
	return current_locale

def get_full_desired_lang_path():
	return os.path.join(sim_paths.get_lang_path(),get_full_language(),"LC_MESSAGES")

def get_languages():
	langs=[]
	langs.append("en_US")
	path=sim_paths.get_lang_path()
	if os.path.isdir(path)==False:
		return False

	for my_dir in os.listdir(path):
		if os.path.isdir(os.path.join(path,my_dir))==True:
			langs.append(my_dir)

	return langs


