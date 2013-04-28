# coding: utf-8
# seapo extensions: special effects
# should be considered as example file

from engine2 import *


class EImage(Image):
	
	def build_effect(self, progress=50):
		'''dim = self.dim
		self.surface.lock()
		for p in itertools.product(range(dim[0]), range(dim[1])):
			color = self.surface.get_at(p)
			if color != (0,0,0,0):
				new_color = (color[0], color[1], color[2], int(alpha*255))
				self.surface.set_at(p, new_color)

		self.surface.unlock()
		return self
		'''
		pass

	def render(self, build=None):
		# caching?
		if build != None:
			img = self.copy().build_effect(build)
		else:
			img = self
			
		return img.render()