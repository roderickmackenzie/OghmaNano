#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#This script 
import os
import sys

from model_api import model_api

class gpvdm_plugin:

	def __init__(self,api):
		a=model_api(verbose=True)
		a.load_snapshots("snapshots")
		#a.edit("light.inp","#light_model","qe")
		#a.edit("jv0.inp","#Vstop","0.8")
		#a.run()