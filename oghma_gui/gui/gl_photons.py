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

## @package gl_photons
#  Shows photons on the device
#


from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from vec import vec

from json_root import json_root

class gl_photons():

	def draw_photon(self,x,y,z,up,r,g,b):
		length=0.9
		glColor4f(r, g, b, 1.0)

		glLineWidth(3)
		wx=np.arange(0, length , 0.025)
		wy=np.sin(wx*3.14159*8)*0.2
		
		start_y=y+length
		stop_y=y

		glBegin(GL_LINES)
		for i in range(1,len(wx)):
			glVertex3f(x, start_y-wx[i-1], z+wy[i-1])
			glVertex3f(x, start_y-wx[i], z+wy[i])

		glEnd()

		if up==False:
			glBegin(GL_TRIANGLES)

			glVertex3f(x-0.1, stop_y,z)
			glVertex3f(x+0.1, stop_y ,z)
			glVertex3f(x,stop_y-0.1 ,z)

			glEnd()
		else:
			glBegin(GL_TRIANGLES)

			glVertex3f(x-0.1, start_y,z)
			glVertex3f(x+0.1, start_y ,z)
			glVertex3f(x,start_y+0.1 ,z)

			glEnd()

	def draw_photons(self,x0,z0):
		if self.gl_main.false_color==True:
			return

		try:
			ray_model=data.sims.ray.segments[0].config.ray_auto_run
		except:
			ray_model=False

		if self.emission==True and ray_model==False:
			den=1.2
			x=np.arange(x0+den/2.0, x0+json_root().electrical_solver.mesh.mesh_x.get_len()*self.scale.x_mul , den)
			z=np.arange(z0+den/2.0, z0+json_root().electrical_solver.mesh.mesh_z.get_len()*self.scale.z_mul , den)

			for i in range(0,len(x)):
				for ii in range(0,len(z)):
					self.draw_photon(x[i]+0.1,y+0.1,z[ii],True,0.0, 0.0, 1.0)

