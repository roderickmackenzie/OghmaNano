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

## @package shape_editor_io
#  This builds the images which are then used to generate shapes
#

import os

from PIL import Image, ImageFilter,ImageOps, ImageDraw
from PIL.ImageQt import ImageQt

from cal_path import get_exe_command
from server import server_get
from cal_path import sim_paths

from math import sin
from math import cos
from math import exp
from math import sqrt

from json_shape_db_item import shape_db_item

class shape_editor_io(shape_db_item):

	def __init__(self):
		shape_db_item.__init__(self)

	def gen_poly(self,x0,y0,dx0,dy0):
		ret=[]
		start=0.0
		stop=360
		steps=6
		dphi_deg=(stop-start)/steps
		phi_deg=start
		while (phi_deg<stop):
			phi=3.1415926*2*phi_deg/360
			dx=sin(phi)*dx0
			dy=cos(phi)*dy0
			ret.append((x0+dx, y0+dy))
			phi_deg=phi_deg+dphi_deg
			#print(phi_deg)
		ret.append(ret[0])
		x_min=1e6
		x_max=0
		y_min=1e6
		y_max=0

		for r in ret:
			if x_min>r[0]:
				x_min=r[0]

			if x_max<r[0]:
				x_max=r[0]

			if y_min>r[1]:
				y_min=r[1]

			if y_max<r[1]:
				y_max=r[1]

		w=x_max-x_min
		#h=y_max-y_min
		h=abs(ret[0][1]-ret[1][1])+abs(ret[1][1]-ret[2][1])
		#seg_len=pow(pow((ret[0][0]-ret[1][0]),2.0)+pow((ret[0][1]-ret[1][1]),2.0),0.5)
		return w,h,ret

	def draw_honeycomb(self):
		dx=self.honeycomb.honeycomb_dx
		dy=self.honeycomb.honeycomb_dy
		shift_x=self.honeycomb.honeycomb_x_shift
		shift_y=self.honeycomb.honeycomb_y_shift
		line_width=self.honeycomb.honeycomb_line_width

		im= Image.new("RGB", (self.image_xlen, self.image_ylen), "#000000")

		x_start=-20
		x_stop=self.image_xlen
		(x_stop-x_start)/dx

		y_start=-20
		y_stop=self.image_ylen
		(y_stop-y_start)/dy

		x_pos=0
		y_pos=0
		delta=0.0
		while(y_pos<y_stop):
			x_pos=delta
			while(x_pos<x_stop):
				#ImageDraw.Draw(im).polygon(, width=7)
				w,h,points=self.gen_poly(shift_x+x_pos,shift_y+y_pos,dx,dy)
				dr=ImageDraw.Draw(im)
				dr.line(points, fill="white", width=line_width)

				x_pos=x_pos+w

			#v_seg_len=2*dy
			y_pos=y_pos+h

			if delta==0.0:
				delta=w/2
			else:
				delta=0

		im=im.rotate(self.honeycomb.honeycomb_rotate)


		return im

	def draw_xtal(self):
		dx=self.xtal.xtal_dx
		dy=self.xtal.xtal_dy
		offset=self.xtal.xtal_offset
		dr=self.xtal.xtal_dr

		im= Image.new("RGB", (self.image_xlen, self.image_ylen), "#000000")
		
		x=dx/2
		y=dy/2
		shift=False
		while(y<self.image_ylen):
			x=0
			if shift==True:
				x=x+offset
			while(x<self.image_xlen):
				drawer=ImageDraw.Draw(im)
				drawer.ellipse([(x-dr, y-dr), (x+dr, y+dr)], fill="white")
				x=x+dx

			shift = not shift

			y=y+dy

		return im

	def draw_lens(self):
		convex=True
		if self.lens.lens_type=="convex":
			convex=True
		else:
			convex=False

		dr=self.image_xlen*self.lens.lens_size*0.5
		do=self.image_xlen*0.5-dr
		im= Image.new("RGB", (self.image_xlen, self.image_ylen), "#000000")
		
		for y in range(0,self.image_ylen):
			for x in range(0,self.image_xlen):
				mag=dr*dr-((x-do)-dr)*((x-do)-dr)-((y-do)-dr)*((y-do)-dr)
				if mag<0:
					mag=0.0
				else:
					mag=sqrt(mag)

				mag=mag/dr
				if convex==True:
					mag=int(255*(mag))
				else:
					mag=int(255-255*(mag))

				im.putpixel((x,y),(mag, mag, mag))

		return im

	def f_square_wave(self,shift,period,x):
		pos=shift+x
		n=int(pos/period)
		if (n % 2) == 0:
			return 0.0
		else:
			return 1.0

	def f_saw_wave(self,shift,period,x):
		pos=shift+x
		n=int(pos/period)
		dx=pos-n*period
		if (n % 2) == 0:
			return (dx/period)
		else:
			return 1.0-(dx/period)

	def draw_saw_wave(self):
		pass

		self.image_xlen/2
		im= Image.new("RGB", (self.image_xlen, self.image_ylen), "#000000")

		for x in range(0,self.image_xlen):
			for y in range(0,self.image_ylen):
			
				if self.saw_wave.shape_saw_type=="saw_wave":
					mag=self.f_saw_wave(self.saw_wave.shape_saw_offset,self.saw_wave.shape_saw_length,x)
				else:
					mag=self.f_square_wave(self.saw_wave.shape_saw_offset,self.saw_wave.shape_saw_length,x)

				mag=int(255*mag)

				im.putpixel((x,y),(mag, mag, mag))

			
		return im

	def add_job_to_server(self,sim_path,server):
		path=os.path.dirname(self.file_name)
		server.add_job(sim_path,"--simmode data@mesh_gen --path \""+path+"\"")

	def load_image(self):
		file_to_load=os.path.join(os.path.dirname(self.file_name),"image.png")
		if os.path.isfile(file_to_load)==False:
			return None

		img=Image.open(file_to_load)
		if img.mode!="RGB":
			img=img.convert('RGB')

		return img.convert('RGB')

	def draw_gauss(self):

		sigma=self.gauss.gauss_sigma
		gauss_offset_x=self.gauss.gauss_offset_x
		gauss_offset_y=self.gauss.gauss_offset_y

		im= Image.new("RGB", (self.image_xlen, self.image_ylen), "#FF0000")

		for y in range(0,self.image_ylen):
			for x in range(0,self.image_xlen):
				mag=int(255*exp(-((x-gauss_offset_x-self.image_xlen/2)/sigma)**2 -((y-gauss_offset_y-self.image_ylen/2)/sigma)**2))
				if self.gauss.gauss_invert==True:
					mag=255-mag
				im.putpixel((x,y),(mag, mag, mag))

		return im

	def new_shape(self,path,info=[]):
		from dlg_get_text2 import dlg_get_text2
		from clone_materials import clone_material
		new_sim_name=dlg_get_text2( _("New shape name:"), _("New shape name"),"add_shape")
		if new_sim_name==None:
			return
		new_sim_name=new_sim_name.ret
	
		if new_sim_name!=None:
			new_shape=os.path.join(path,new_sim_name)
			ret=clone_material(new_shape,sim_paths.get_shape_template_path())
			self.save_as(os.path.join(new_shape,"data.json"))
			if ret==False:
				error_dlg(self,_("I cant write to:")+new_shape+" "+_("This means either the disk is full or your system administrator has not given you write permissions to that location."))
				return None

			return new_shape

		return None

	def merge_shapes(self,path,info=[]):
		from dlg_get_text2 import dlg_get_text2
		from clone_materials import clone_material
		dlg_obj=dlg_get_text2( _("New shape name"), "","add_shape",info=info,title_text=_("Merge shapes to new"))
		if dlg_obj==None:
			return
			
		new_sim_name=dlg_obj.ret[0]
		
		if new_sim_name!=None:
			new_shape=os.path.join(path,new_sim_name)
			ret=clone_material(new_shape,sim_paths.get_shape_template_path())
			self.save_as(os.path.join(new_shape,"data.json"))
			if ret==False:
				error_dlg(self,_("I cant write to:")+new_shape+" "+_("This means either the disk is full or your system administrator has not given you write permissions to that location."))
				return None

			return new_shape,dlg_obj.ret[1],dlg_obj.ret[2]

		return None
