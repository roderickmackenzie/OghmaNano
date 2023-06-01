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

## @package json_world_stats
#  Used to calculate the size of the world
#

from vec import vec

class json_world_stats():

	def get_world_size(self):
		my_min=vec()
		my_max=vec()

		if self.world.config.world_automatic_size==False:
			my_min.x=self.world.config.world_x0
			my_min.y=self.world.config.world_y0
			my_min.z=self.world.config.world_z0

			my_max.x=self.world.config.world_x1
			my_max.y=self.world.config.world_y1
			my_max.z=self.world.config.world_z1
		else:

			my_min.x=1e6
			my_min.y=1e6
			my_min.z=1e6

			my_max.x=-1e6
			my_max.y=-1e6
			my_max.z=-1e6
			for l in self.epi.layers:
				my_min,my_max=l.get_min_max(my_min,my_max)

			for l in self.world.world_data.segments:
				if l.name!="label":
					my_min,my_max=l.get_min_max(my_min,my_max)

			for source in self.optical.light_sources.lights.segments:
				if source.light_illuminate_from=="xyz":
					my_min,my_max=source.get_min_max(my_min,my_max)

			for source in self.optical.detectors.segments:
				my_min,my_max=source.get_min_max(my_min,my_max)

			dx0=(self.world.config.world_margin_x0-1.0)*(my_max.x-my_min.x)
			dx1=(self.world.config.world_margin_x1-1.0)*(my_max.x-my_min.x)

			dy0=(self.world.config.world_margin_y0-1.0)*(my_max.y-my_min.y)
			dy1=(self.world.config.world_margin_y1-1.0)*(my_max.y-my_min.y)

			dz0=(self.world.config.world_margin_z0-1.0)*(my_max.z-my_min.z)
			dz1=(self.world.config.world_margin_z1-1.0)*(my_max.z-my_min.z)

			my_min.x=my_min.x-dx0
			my_min.y=my_min.y-dy0
			my_min.z=my_min.z-dz0

			my_max.x=my_max.x+dx1
			my_max.y=my_max.y+dy1
			my_max.z=my_max.z+dz1

		return my_min,my_max


