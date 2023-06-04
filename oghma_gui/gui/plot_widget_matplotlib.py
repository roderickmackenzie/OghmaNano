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

## @package plot_widget
#  The main plot widget.
#

from __future__ import unicode_literals

import os
from numpy import *


#matplotlib
import matplotlib
from matplotlib import cm
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.pyplot import colorbar
from matplotlib.colors import LogNorm

from util_latex import latex
from util import pygtk_to_latex_subscript
from color_map import get_color
from color_map import get_color_black
from color_map import get_marker
from util import fx_with_units
from util import time_with_units

from matplotlib.ticker import ScalarFormatter
from lock import get_lock
from sim_name import sim_name
from math import isnan
from bytes2str import bytes2str

class plot_widget_matplotlib():

	def matplotlib_do_plot(self):
		if len(self.data)==0:
			return

		if self.data[0].valid_data==False:
			return

		if self.data[0].type=="poly":
			return

		key_text=[]

		self.plot_type=""
		#print("OK ",self.data[0].type)
		#print(self.data[0].x_len,self.data[0].z_len,self.data[0].data)

		if self.data[0].type==b"yrgb" or self.data[0].cols==b"zxrgb":
			self.plot_type="rgb"
		elif self.data[0].type==b"quiver":
			self.plot_type="quiver"
		else:
			if self.data[0].x_len==1 and self.data[0].z_len==1:
				self.plot_type="linegraph"
			elif self.data[0].x_len>1 and self.data[0].y_len>1 and self.data[0].z_len==1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len>1 and self.data[0].y_len==1 and self.data[0].z_len>1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len==1 and self.data[0].y_len>1 and self.data[0].z_len>1:
				if self.data[0].type==b"3d":
					self.plot_type="wireframe"
				if self.data[0].type==b"heat":
					self.plot_type="heat"
			elif self.data[0].x_len>1 and self.data[0].y_len>1 and self.data[0].z_len>1:
				print("ohhh full 3D")
				self.plot_type="3d"
			else:
				print(_("I don't know how to process this type of file!"),self.data[0].x_len, self.data[0].y_len,self.data[0].z_len)
				return

		self.setup_axis()


		all_plots=[]
		files=[]
		my_max=1.0
		
		if self.plot_type=="linegraph":		#This is for the 1D graph case
			self.ax[0].set_xlabel(self.data[0].y_label.decode()+" ("+self.data[0].y_units.decode()+")")
			self.ax[0].set_ylabel(self.data[0].data_label.decode()+" ("+self.data[0].data_units.decode()+")")
	
			for i in range(0,len(self.data)):
				if self.data[0].logy==True:
					self.ax[i].set_xscale("log")

				if self.data[0].logdata==True:
					self.ax[i].set_yscale("log")

				if isnan(self.data[i].data_min)==False and isnan(self.data[i].data_max)==False:
					self.ax[i].set_ylim([self.data[i].data_min,self.data[i].data_max])
				if self.data[i].rgb_to_hex()!=None:
					col="#"+self.data[i].rgb_to_hex()
				else:
					col=get_color(i)
				cur_plot, = self.ax[i].plot(self.data[i].y_scale,self.data[i].data[0][0], linewidth=3 ,alpha=1.0,color=col,marker=get_marker(i))
				#print(self.data[i].y_scale,self.data[i].data[0][0])
				if self.data[i].key_text!="":
					key_text.append("$"+latex().numbers_to_latex(bytes2str(self.data[i].key_text))+ " "+pygtk_to_latex_subscript(bytes2str(self.data[0].key_units)) +"$")

				all_plots.append(cur_plot)
				
				if len(self.data[i].labels)!=0:
					#we only want this many data labels or it gets crowded
					max_points=12
					n_points=range(0,len(self.data[i].y_scale))
					if len(n_points)>max_points:
						step=int(len(n_points)/max_points)
						n_points=[]
						pos=0
						while(len(n_points)<max_points):
							n_points.append(pos)
							pos=pos+step

					for ii in n_points:
						label_text=self.data[i].labels[ii]
						self.ax[i].annotate(label_text,xy = (self.data[i].y_scale[ii], self.data[i].data[0][0][ii]), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))


				#print(self.data[i].labels)
		elif self.plot_type=="wireframe":

			if self.data[0].cols==b"xzd":
				self.ax[0].set_xlabel('\n'+bytes2str(self.data[0].x_label)+'\n ('+bytes2str(self.data[0].x_units)+")")
				self.ax[0].set_ylabel('\n'+bytes2str(self.data[0].z_label)+'\n ('+bytes2str(self.data[0].z_units)+")")
				self.ax[0].set_zlabel('\n'+bytes2str(self.data[0].data_label)+'\n ('+bytes2str(self.data[0].data_units)+")")
			else:
				self.ax[0].set_xlabel('\n'+bytes2str(self.data[0].x_label)+'\n ('+bytes2str(self.data[0].x_units)+")")
				self.ax[0].set_ylabel('\n'+bytes2str(self.data[0].y_label)+'\n ('+bytes2str(self.data[0].y_units)+")")
				self.ax[0].set_zlabel('\n'+bytes2str(self.data[0].data_label)+'\n ('+bytes2str(self.data[0].data_units)+")")

			self.log_3d_workaround()

			if self.force_data_max==False:
				my_max,my_min=self.data[0].max_min()
				for i in range(0,len(self.data)):
					my_max,my_min=self.data[i].max_min(cur_min=my_min,cur_max=my_max)
			else:
				my_max=self.force_data_max
				my_min=self.force_data_min
			#print(self.force_data_max,my_min,my_max)
			self.ax[0].set_zlim(my_min, my_max)

			for i in range(0,len(self.data)):

				if self.data[i].logx==True:
					self.ax[i].set_xscale("log")

				if self.data[i].logy==True:
					self.ax[i].set_yscale("log")

				#if self.data[i].key_text!="":
				key="$"+latex().numbers_to_latex(bytes2str(self.data[i].key_text))+ " "+pygtk_to_latex_subscript(bytes2str(self.data[0].key_units)) +"$"

				if self.data[i].cols==b"xzd":
					X, Y = meshgrid( self.data[i].z_scale,self.data[i].x_scale)
					Z=array(self.data[i].data)
					#a=Z.flatten(len(self.data[i].z_scale),len(self.data[i].x_scale))
					#a.reshape()
					Z = reshape(self.data[i].data,(len(self.data[i].z_scale),len(self.data[i].x_scale)))
				elif self.data[i].cols==b"yzd":
					X, Y = meshgrid( self.data[i].z_scale,self.data[i].y_scale)
					#Z = self.data[i].data[0]
					Z=array(self.data[i].data)
					Z = reshape(self.data[i].data,(len(self.data[i].z_scale),len(self.data[i].y_scale)))
				else:
					X, Y = meshgrid( self.data[i].y_scale,self.data[i].x_scale)
					Z = self.data[i].data[0]
					Z = array(Z)

				# Plot the surface
				if self.data[i].r==-1:
					col=get_color(i)
				else:
					col=[self.data[i].r, self.data[i].g, self.data[i].b]

				#print(self.data[i].plot_type,"here")
				if self.data[i].plot_type=="wireframe" or self.data[i].plot_type=="":
					if self.show_key==False:
						key=None
					try:
						im=self.ax[0].plot_wireframe( Y,X, Z,color=col, label=key, clip_on=True)
					except:
						print("MATPLOT error in plot_widget_matplotlib")
				elif self.data[i].plot_type=="contour":
					im=self.ax[0].contourf( Y,X, Z,cmap="inferno")	#,color=col
				elif self.data[i].plot_type=="heat":
					my_max,my_min=self.data[0].max_min()
					im=self.ax[0].plot_surface(Y,X, Z, linewidth=0, vmin=my_min, vmax=my_max,cmap="inferno", antialiased=False)
					#hsv
				self.ax[0].legend()
				#im=self.ax[0].contourf( Y,X, Z,color=col)

#cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
		elif self.plot_type=="heat":
			self.ax[0].set_xlabel(self.data[0].y_label.decode()+" ("+self.data[0].y_units.decode()+")")
			self.ax[0].set_ylabel(self.data[0].x_label.decode()+" ("+self.data[0].x_units.decode()+")")
			my_max,my_min=self.data[0].max_min()
			for i in range(0,len(self.data)):
				if self.data[i].logdata==True:
					if my_min==0:
						my_min=1.0
					im=self.ax[0].pcolor(self.data[i].y_scale,self.data[i].x_scale,self.data[i].data[0], norm=LogNorm(vmin=my_min, vmax=my_max), vmin=my_min, vmax=my_max,cmap="gnuplot")
				else:
					im=self.ax[0].pcolormesh(self.data[i].y_scale,self.data[i].x_scale,self.data[i].data[0], vmin=my_min, vmax=my_max,cmap="gnuplot")

				self.cb=self.fig.colorbar(im)

		elif self.plot_type=="3d":
			self.ax[0].set_xlabel(self.data[0].x_label.decode()+" ("+self.data[0].x_units.decode()+")")
			self.ax[0].set_ylabel(self.data[0].y_label.decode()+" ("+self.data[0].y_units.decode()+")")
			i=0
			y_scale=self.data[i].y_scale
			x_scale=self.data[i].x_scale

			X, Y = meshgrid( y_scale,x_scale)		#self.data[i].y_scale,self.data[i].x_scale
			Z = self.data[i].data[0]
			col=get_color(i)
			my_max,my_min=self.data[0].max_min()
		elif self.plot_type=="rgb":
			if self.data[0].cols==b"yrgb":
				self.ax[0].set_xlabel(self.data[0].y_label.decode()+" ("+self.data[0].y_units.decode()+")")
				self.ax[0].set_ylabel(self.data[0].data_label.decode()+" ("+self.data[0].data_units.decode()+")")
				self.ax[0].imshow(self.data[0].data[0],extent=[self.data[0].y_scale[0],self.data[0].y_scale[-1],self.data[0].y_scale[0]/4,self.data[0].y_scale[-1]/4])
			elif self.data[0].cols==b"zxrgb":
				self.ax[0].set_xlabel(self.data[0].z_label.decode()+" ("+self.data[0].z_units.decode()+")")
				self.ax[0].set_ylabel(self.data[0].x_label.decode()+" ("+self.data[0].x_label.decode()+")")
				self.ax[0].imshow(self.data[0].data)
				#,extent=[self.data[0].z_scale[0],self.data[0].z_scale[-1],self.data[0].x_scale[0], self.data[0].x_scale[-1]]
				#print(self.data[0].data)
				#
			#plt.xticks([0,90,180])
			#,extent=[self.data[0].y_scale[0],self.data[0].y_scale[-1],0,20]
		elif self.plot_type=="quiver":
			self.ax[0].set_xlabel(self.data[0].x_label.decode()+" ("+self.data[0].x_units.decode()+")")
			self.ax[0].set_ylabel(self.data[0].y_label.decode()+" ("+self.data[0].y_units.decode()+")")
			self.ax[0].set_zlabel(self.data[0].z_label.decode()+" ("+self.data[0].z_units.decode()+")")
			X=[]
			Y=[]
			Z=[]
			U=[]
			V=[]
			W=[]
			mag=[]
			for d in self.data[0].data:
				X.append(d.x)
				Y.append(d.y)
				Z.append(d.z)
				U.append(d.dx)
				V.append(d.dy)
				W.append(d.dz)
				mag.append(d.mag)

			c=plt.cm.hsv(mag)

			mag=[]
			for d in self.data[0].data:

				mag.append(2.0)

			self.ax[0].quiver(X, Y, Z, U, V, W,colors=c,linewidths=mag)
			self.ax[0].set_xlim([0, self.data[0].xmax])
			self.ax[0].set_ylim([0, self.data[0].ymax])
			self.ax[0].set_zlim([0, self.data[0].zmax])


		#setup the key
		if self.data[0].legend_pos=="No key":
			self.ax[i].legend_ = None
		else:
			if len(files)<40:
				self.fig.legend(all_plots, key_text, self.data[0].legend_pos)

		if get_lock().encode_output==True:
			x=0.8
			y=0.25
			#while(x<1.0):
			#	y=0
			#	while(y<1.0):
			self.fig.text(x, y, "Upgrade to "+sim_name.name+" professional today!", fontsize=20, color='gray', ha='right', va='bottom', alpha=0.05)

			#		y=y+0.2
			#	x=x+0.4

		if self.show_title==True:
			
			title=bytes2str(self.data[0].title)
			if self.data[0].time!=-1.0 and self.data[0].Vexternal!=-1.0:
				mul,unit=time_with_units(self.data[0].time)
				if isnan(self.data[0].Vexternal)==False:
					voltage_text=" V="+str(self.data[0].Vexternal)+" "
				else:
					voltage_text=""

				if isnan(self.data[0].Vexternal)==False:
					time_text=_("time")+"="+str(self.data[0].time*mul)+" "+unit
				else:
					time_text=""

				title=title+voltage_text+time_text

			self.fig.suptitle(title)

			self.setWindowTitle(title+sim_name.web_window_title)
		else:
			self.fig.suptitle("")

		self.fig.canvas.draw()

	def matplotlib_norm_data(self):

		if len(self.data)>0:
			if self.data[0].type==b"yrgb" or self.data[0].type==b"quiver" or self.data[0].type==b"poly":
				return

			if self.data[0].type==b"zxrgb":
				#for i in range(0,len(self.data)):
				#	for x in range(0,self.data[i].x_len):
				#		self.data[i].x_scale[x]=self.data[i].x_scale[x]*self.data[i].x_mul

				#	for z in range(0,self.data[i].z_len):
				#		self.data[i].z_scale[z]=self.data[i].z_scale[z]*self.data[i].z_mul

				return

			if self.data[0].data==None:
				return

			if self.zero_frame_enable==True:
				if len(self.data)>1:
					for i in range(1,len(self.data)):
						dat_file_sub(self.data[i],self.data[0])
					
					dat_file_sub(self.data[0],self.data[0])
			for i in range(0,len(self.data)):
				for x in range(0,self.data[i].x_len):
					self.data[i].x_scale[x]=self.data[i].x_scale[x]*self.data[i].x_mul

				for y in range(0,self.data[i].y_len):
					self.data[i].y_scale[y]=self.data[i].y_scale[y]*self.data[i].y_mul

				for z in range(0,self.data[i].z_len):
					self.data[i].z_scale[z]=self.data[i].z_scale[z]*self.data[i].z_mul

				for x in range(0,self.data[i].x_len):
					for y in range(0,self.data[i].y_len):
						for z in range(0,self.data[i].z_len):
							self.data[i].data[z][x][y]=self.data[i].data[z][x][y]*self.data[i].data_mul

			if self.data[0].invert_y==True:
				for i in range(0,len(self.data)):
					dat_file_mul(self.data[i],-1)

			if self.data[0].subtract_first_point==True:
				val=self.data[0].data[0][0][0]
				for i in range(0,len(self.data)):
					dat_file_sub_float(self.data[i],val)


			if self.data[0].add_min==True:
				my_max,my_min=self.data[0].max_min()
				for i in range(0,len(self.data)):
					dat_file_sub_float(self.data[i],my_min)


	def setup_axis(self):
		this_plot=[]
		for d in self.data:
			this_plot.append(os.path.basename(d.file_name)) 

		if (this_plot==self.last_plot)==False:
			#print("redoooo!!!!!!!!!!!!!")
			self.fig.clf()
			self.fig.subplots_adjust(bottom=0.2)
			self.fig.subplots_adjust(bottom=0.2)
			self.fig.subplots_adjust(left=0.1)
			self.fig.subplots_adjust(hspace = .001)

			self.ax=[]

			if self.plot_type=="linegraph":
				ax1=None
				for i in range(0,len(self.data)):
					axis="y1"
					if i==0:
						ax1=self.fig.add_subplot(111,facecolor='white')

					if len(self.y1_y2)>i:
						if self.y1_y2[i]=="y2":
							axis="y2"
					if axis=="y1":
						self.ax.append(ax1)
					else:
						self.ax.append(self.ax[-1].twinx())

					y_formatter = ScalarFormatter(useOffset=False)
					self.ax[-1].yaxis.set_major_formatter(y_formatter)

			elif self.plot_type=="rgb":
				for i in range(0,len(self.data)):
					self.ax.append(self.fig.add_subplot(111,facecolor='white'))
			elif self.plot_type=="wireframe":
				self.ax=[self.fig.add_subplot(111,facecolor='white' ,projection='3d')]
				self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

			elif self.plot_type=="heat":
				for i in range(0,len(self.data)):
					self.ax.append(self.fig.add_subplot(111,facecolor='white'))
			elif self.plot_type=="3d":
				for i in range(0,len(self.data)):
					self.ax.append(self.fig.add_subplot(111,facecolor='white' ,projection='3d'))
			elif self.plot_type=="quiver":
				for i in range(0,len(self.data)):
					self.ax.append(self.fig.add_subplot(111,facecolor='white' ,projection='3d'))
		else:
			if self.plot_type=="3d":
				for a in self.ax:
					for c in a.collections:
						c.remove()
			elif self.plot_type=="linegraph":
				for a in self.ax:
					a.clear()
			elif self.plot_type=="heat":
				for a in self.ax:
					a.clear()
				if self.cb!=None:
					self.cb.remove()
					self.cb=None
			else:
				for a in self.ax:
					a.clear()

		self.last_plot=[]
		for d in self.data:
			self.last_plot.append(os.path.basename(d.file_name))
