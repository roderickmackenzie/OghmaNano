#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from oghma_api import oghma_api

def run():
	a=oghma_api(verbose=True)
	a.set_save_dir(device_data)
	a.edit("light.inp","#light_model","qe")
	a.edit("jv0.inp","#Vstop","0.8")
	a.run()