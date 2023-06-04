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

## @package colors
#  Functions to deal with colors.
#

color=[]
color_black=[]
marker=[]

def gen_colors_black():
	global color_black
	global marker

	base=[[0.0,0.0,0.0]]
	marker=[]
	color_black=[]
	for i in range(0,100):
		color_black.append([base[0][0],base[0][1],base[0][2]])
		marker.append("")

def gen_colors():
	global color
	global marker
	base=[[0.0,0.0,1.0],[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,1.0,1.0],[1.0,1.0,0.0],[1.0,0.0,1.0]]
	marker=[]
	mul=1.0
	color=[]
	for rounds in range(0,20):
		for i in range(0,len(base)):
			color.append([base[i][0]*mul,base[i][1]*mul,base[i][2]*mul])
			marker.append("")
		mul=mul*0.5

gen_colors()
gen_colors_black()

def get_color(i):
	global color
	return color[i]

def get_color_black(i):
	global color_black
	return color_black[i]

def get_marker(i):
	global marker
	return marker[i]

class color_map():

	def __init__(self,map_name="inferno"):
		#[(0.0,0.0,0.0), (255.0,255.0,0.0), (0.0,255.0,0.0), (0.0,255.0,255.0), (0.0,0.0,255.0)]
		#points = [(0.0,0.0,0.0),  (0.0,0.0,255.0),  (255.0,0.0,0.0)]
		#inferno
		points=[]
		if map_name=="inferno":
			points.append("000004") # black
			points.append("1f0c48") # dark purple
			points.append("550f6d") # dark purple
			points.append("88226a") # purple
			points.append("a83655") # red-magenta
			points.append("e35933") # red
			points.append("f9950a") # orange
			points.append("f8c932") # yellow-orange
			points.append("fcffa4") # light yellow

		elif map_name=="blues":
			points.append("440154")
			points.append("472c7a")
			points.append("3b518b")
			points.append("2c718e")
			points.append("21908d")
			points.append("27ad81")
			points.append("5cc863")
			points.append("aadc32")
			points.append("fde725")
		elif map_name=="matlab_jet":
			points.append("000090")
			points.append("000fff")
			points.append("0090ff")
			points.append("0fffee")
			points.append("90ff70")
			points.append("ffee00")
			points.append("ff7000")
			points.append("ee0000")
			points.append("7f0000")
		elif map_name=="matlab":
			self.map=[[53,42,135],[54,48,147],[54,55,160],[53,61,173],[50,67,186],[44,74,199],[32,83,212],[15,92,221],[3,99,225],[2,104,225],[4,109,224],[8,113,222],[13,117,220],[16,121,218],[18,125,216],[20,129,214],[20,133,212],[19,137,211],[16,142,210],[12,147,210],[9,152,209],[7,156,207],[6,160,205],[6,164,202],[6,167,198],[7,169,194],[10,172,190],[15,174,185],[21,177,180],[29,179,175],[37,181,169],[46,183,164],[56,185,158],[66,187,152],[77,188,146],[89,189,140],[101,190,134],[113,191,128],[124,191,123],[135,191,119],[146,191,115],[156,191,111],[165,190,107],[174,190,103],[183,189,100],[192,188,96],[200,188,93],[209,187,89],[217,186,86],[225,185,82],[233,185,78],[241,185,74],[248,187,68],[253,190,61],[255,195,55],[254,200,50],[252,206,46],[250,211,42],[247,216,38],[245,222,33],[245,228,29],[245,235,24],[246,243,19],[249,251,14]]
			return
		self.map = []
		delta=255/(len(points)-1)
		count=0
		pos=0
		for i in range(0, 256):
			if count>delta:
				pos=pos+1
				count=0

			#print(i,pos)
			ratio=count/delta

			c0 = [int(points[pos][0:2], base=16),int(points[pos][2:4], base=16),int(points[pos][4:6], base=16)]
			c1 = [int(points[pos+1][0:2], base=16),int(points[pos+1][2:4], base=16),int(points[pos+1][4:6], base=16)]
			#c0=points[pos]
			#c1=points[pos+1]

			r=c0[0]+(c1[0]-c0[0])*ratio
			g=c0[1]+(c1[1]-c0[1])*ratio
			b=c0[2]+(c1[2]-c0[2])*ratio

			count=count+1

			self.map.append([int(r), int(g), int(b)])


