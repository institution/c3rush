# coding: utf-8

import geometry as geo
import render as ren

class Box(geo.Box, ren.Box):
	pass	

class PBox(geo.PBox, ren.PBox):
	pass
	
class GridBox(geo.GridBox, ren.PBox):
	pass

class CBox(geo.CBox, ren.CBox):
	pass
	
class TextBox(geo.TextBox, ren.TextBox):
	pass
			
class VBox(geo.VBox, ren.VBox):
	pass







