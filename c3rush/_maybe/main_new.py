# coding: utf-8
import sys
import pyglet
from pyglet import clock
from math import cos, sin, pi
from pyglet.gl import *
from pyglet import font
from pyglet.font import GlyphString, Text


pyglet.text.Label


class View(object):
	def __init__(self, model, window):
		self.model, self.window = model, window

	def set_projection(self):
		glEnable(GL_BLEND)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-200, 200, -200, 200, -200, 200)
		glMatrixMode(GL_MODELVIEW)

	def render(self, dt):
		self.window.clear()
		
		self.set_projection()
		
		font.add_file('./font/Pure-ThinDuranGo.ttf')
		arial = font.load('Roman', 9, dpi=96)
		
		text = 'Hello, world!'
		glyphs = arial.get_glyphs(text)

		#gs = GlyphString(text, glyphs)
		# glyph_string.draw()
		#for g in gs:
		#	g.blit(x, y, z=0, width=None, height=None)


		label = pyglet.text.Label('Hello, world a',
			#font_name='./font/Pure-ThinDuranGo.ttf',
			font_size=14,
			x=10, y=10
		)
		label.draw()

		#glBegin(GL_LINES)
		#for ob in self.model:
		#	self.render_ob(*ob)
		#glEnd()

		self.window.flip()


def main():
	window = pyglet.window.Window(
		width=400, height=400
	)

	model = None
	view = View(model, window)

	#clock.schedule_interval(model.update, 0.001)
	clock.schedule(view.render)

	pyglet.app.run()


if __name__ == '__main__':
	main()

